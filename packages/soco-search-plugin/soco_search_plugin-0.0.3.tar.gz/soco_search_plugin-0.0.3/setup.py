import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="soco_search_plugin",
    packages = find_packages(),
    include_package_data=True,
    version="0.0.3",
    author="kyusonglee",
    description="Soco search plugin helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.soco.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'requests >= 2.23.0',
        "flask",
        "flask_cors",
        "soco-clip",
        "grpcio>=1.34.0",
        "grpcio-tools>=1.34.0"
    ]
)
