from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openclaw-verifier",
    version="0.2.0",
    author="OpenClaw Verifier Team",
    author_email="openclaw-verifier@example.com",
    description="Security verification tool for OpenClaw Skills",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openclaw-verifier/openclaw-verifier",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "openclaw-verifier=cli:main",
        ],
    },
)

