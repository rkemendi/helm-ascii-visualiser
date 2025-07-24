import os
import subprocess
import sys
import yaml
from collections import defaultdict
from rich.console import Console
from rich.tree import Tree

console = Console()

def render_helm_chart(chart_path):
    """Render Helm chart into YAML manifests."""
    try:
        result = subprocess.run(
            ["helm", "template", chart_path],
            capture_output=True,
            text=True,
            check=True
        )
        return list(yaml.safe_load_all(result.stdout))
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Helm error:[/red] {e.stderr}")
        sys.exit(1)

def index_resources(docs):
    """Index resources by kind and name."""
    resources = defaultdict(list)
    resource_map = {}

    for doc in docs:
        if not isinstance(doc, dict):
            continue
        kind = doc.get("kind")
        metadata = doc.get("metadata", {})
        name = metadata.get("name")
        if not (kind and name):
            continue
        resources[kind].append(doc)
        resource_map[(kind, name)] = doc
    return resources, resource_map

def match_service_to_deployment(service, deployments):
    """Match a Service to a Deployment via label selectors."""
    selector = service.get("spec", {}).get("selector", {})
    matched = []
    for dep in deployments:
        labels = dep.get("spec", {}).get("template", {}).get("metadata", {}).get("labels", {})
        if all(item in labels.items() for item in selector.items()):
            matched.append(dep["metadata"]["name"])
    return matched

def extract_deployment_links(deployment):
    """Find ConfigMaps, Secrets, and SA used by the Deployment."""
    used = defaultdict(set)
    spec = deployment.get("spec", {})
    template = spec.get("template", {})
    pod_spec = template.get("spec", {})
    containers = pod_spec.get("containers", [])

    # ServiceAccount
    sa = pod_spec.get("serviceAccountName")
    if sa:
        used["ServiceAccount"].add(sa)

    # Volumes
    for vol in pod_spec.get("volumes", []):
        cm = vol.get("configMap", {})
        if cm.get("name"):
            used["ConfigMap"].add(cm["name"])
        secret = vol.get("secret", {})
        if secret.get("secretName"):
            used["Secret"].add(secret["secretName"])

    # Environment vars
    for container in containers:
        envs = container.get("env", [])
        for env in envs:
            val = env.get("valueFrom", {})
            if "configMapKeyRef" in val:
                used["ConfigMap"].add(val["configMapKeyRef"]["name"])
            if "secretKeyRef" in val:
                used["Secret"].add(val["secretKeyRef"]["name"])

    return used

def build_tree(resources):
    """Construct an ASCII tree showing resources and connections."""
    tree = Tree("📦 [bold cyan]Kubernetes Resources[/bold cyan]")

    # Index deployments
    deployments = resources.get("Deployment", [])
    services = resources.get("Service", [])

    # Map for tracking links
    links = {}

    # Build deployment ➝ X relationships
    for dep in deployments:
        name = dep["metadata"]["name"]
        deps = extract_deployment_links(dep)
        links[name] = deps

    # Build service ➝ deployment links
    service_links = {}
    for svc in services:
        svc_name = svc["metadata"]["name"]
        matched = match_service_to_deployment(svc, deployments)
        service_links[svc_name] = matched

    # Tree: Deployments with their connections
    dep_node = tree.add("[yellow]Deployments[/yellow]")
    for dep in deployments:
        dep_name = dep["metadata"]["name"]
        dnode = dep_node.add(f"[green]{dep_name}[/green]")

        for kind, names in links.get(dep_name, {}).items():
            for n in names:
                dnode.add(f"🔗 {kind}: [blue]{n}[/blue]")

    # Tree: Services and their matched deployments
    svc_node = tree.add("[yellow]Services[/yellow]")
    for svc in services:
        svc_name = svc["metadata"]["name"]
        snode = svc_node.add(f"[green]{svc_name}[/green]")
        for d in service_links.get(svc_name, []):
            snode.add(f"↪️ Targets Deployment: [blue]{d}[/blue]")

    # Tree: Other Resources
    for kind in sorted(resources):
        if kind in ["Deployment", "Service"]:
            continue
        knode = tree.add(f"[yellow]{kind}s[/yellow]")
        for obj in resources[kind]:
            knode.add(f"[green]{obj['metadata']['name']}[/green]")

    console.print(tree)

def main():
    if len(sys.argv) != 2:
        console.print("[bold red]Usage:[/bold red] python helm_ascii_visualizer.py <chart_path>")
        sys.exit(1)

    chart_path = sys.argv[1]
    if not os.path.isdir(chart_path):
        console.print(f"[red]Invalid chart path:[/red] {chart_path}")
        sys.exit(1)

    console.print(f"[blue]Rendering Helm chart:[/blue] {chart_path}")
    docs = render_helm_chart(chart_path)
    resources, _ = index_resources(docs)
    build_tree(resources)

if __name__ == "__main__":
    main()