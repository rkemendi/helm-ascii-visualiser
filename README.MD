# 🧭 Helm ASCII Visualizer

[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Helm](https://img.shields.io/badge/helm-3.x-blue.svg)](https://helm.sh)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/helm-ascii-visualizer/pulls)

> Visualize Kubernetes resources from a Helm chart — beautifully, in your terminal.

---

## ✨ Features

- 📦 Renders Helm charts using `helm template`
- 🔍 Parses Kubernetes manifests and groups resources
- 🔗 Shows connections:
  - `Deployment ➝ ConfigMap`, `Secret`, `ServiceAccount`
  - `Service ➝ Deployment` via label selectors
- 🎨 ASCII-based, rich-text tree output
- ⚡️ Fast and zero-cluster access needed

---

## 📸 Example Output

📦 Kubernetes Resources
├── Deployments
│ └── mychart-deployment
│ ├── 🔗 ConfigMap: mychart-config
│ └── 🔗 ServiceAccount: mychart-sa
├── Services
│ └── mychart-service
│ └── ↪️ Targets Deployment: mychart-deployment
├── ConfigMaps
│ └── mychart-config
├── ServiceAccounts
│ └── mychart-sa


---

## 🚀 Getting Started

### 🔧 Prerequisites

- [Python 3.7+](https://www.python.org/)
- [Helm 3.x](https://helm.sh/)
- Python packages:

```bash
pip install pyyaml rich

▶️ Usage
python helm_ascii_visualizer.py ./path-to-your-helm-chart
Replace ./path-to-your-helm-chart with the path to the Helm chart you want to visualize.

🧠 How It Works

Runs helm template to render raw YAML manifests.
Parses the output with PyYAML.
Builds a resource graph from:
Metadata and spec fields
Labels and selectors
Volume mounts and environment sources
Renders everything as a visual tree using the rich console library.
📁 Project Structure

helm_ascii_visualizer.py   # Main script
README.md                  # You are here 📍
🛠️ Customization Ideas

Export visualization to Graphviz or Mermaid
Build a web UI (D3.js or React + Tailwind)
Add CRD support
Export to Markdown or PDF
🤝 Contributing

Pull requests, issues, and suggestions are welcome!
Feel free to fork the repo and improve it.

📄 License

MIT License

❤️ Author The Bloody AI revolution aka ChatGPT

“Good architecture is invisible — but now it's ASCII art.” 🎨