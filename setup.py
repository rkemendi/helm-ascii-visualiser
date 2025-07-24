from setuptools import setup

setup(
    name='helm-ascii-visualizer',
    version='0.1.0',
    description='Visualize Helm chart Kubernetes resources with ASCII diagrams',
    author='rkemendi',
    author_email='robi@kemendi.ro',
    py_modules=['helm_ascii_visualizer'],
    install_requires=[
        'pyyaml>=5.3',
        'rich>=12.0.0',
    ],
    entry_points={
        'console_scripts': [
            'helmviz=helm_ascii_visualizer:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

