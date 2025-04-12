from setuptools import setup, find_packages

setup(
    name="funneler",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["funneler"],
    install_requires=[
        "typer[all]>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "funneler=funneler:app",
        ],
    },
    author="Evan",
    description="A CLI tool to share directories via Tailscale Funnel",
    keywords="tailscale, funnel, file sharing",
    python_requires=">=3.6",
)
