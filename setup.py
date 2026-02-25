# setup.py
from setuptools import setup, find_packages

setup(
    name="openclaw-verifier",
    version="0.1.0",
    description="Security verification tool for OpenClaw Skills",
    author="OpenClaw Verifier Team",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "openclaw-verifier=cli:main",
        ],
    },
    python_requires=">=3.8",
)
