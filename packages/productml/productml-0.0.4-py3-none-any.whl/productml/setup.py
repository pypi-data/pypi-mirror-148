import os

from setuptools import setup, find_packages

NAME = "productml"
VERSION = "0.0.4"
DESCRIPTION = "Library for Akumyn product-level inference."

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def get_dependencies(path: str) -> str:
    dependencies = []
    if os.path.isfile(path):
        with open(path) as f:
            dependencies = f.read().splitlines()
    return dependencies

def get_readme(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

install_requires = get_dependencies(ROOT_PATH + '/../requirements.txt')
long_desc = get_readme(ROOT_PATH + '/../README.md')

print(f"os.getcwd(): {os.getcwd()}")
print(f"ROOT_PATH: {ROOT_PATH}")
print(f"install_requires: {install_requires}")

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="DevsDoData",
    author_email="jerryyexu@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.7",
    keywords="retail, ml, cv, devsdodata",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)