from setuptools import setup, find_packages

setup(
    name="ml-chip-design-automation",
    version="2.4.1",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    install_requires=[
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "pytest>=7.4.0",
    ],
)