from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Fumagalli_Motta_Tarantino_2020",
    packages=find_packages(exclude=["Notebooks"]),
    version="0.1.2",  # change with new version
    license="MIT",
    description="Implements the models presented in Fumagalli et al. (2020)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Manuel Bieri",
    author_email="manuel.bieri@outlook.com",
    url="https://github.com/manuelbieri/Fumagalli_2020#readme",
    project_urls={
        "Documentation": "https://manuelbieri.ch/Fumagalli_2020/",
        "Download": "https://github.com/manuelbieri/Fumagalli_2020/releases",
        "Source": "https://github.com/manuelbieri/Fumagalli_2020",
    },
    download_url="https://github.com/manuelbieri/Fumagalli_2020/archive/refs/tags/v0.1.2.tar.gz",  # change with new version
    keywords=["Killer Acquisition", "Competition", "Innovation"],
    classifiers=[
        "Development Status :: 3 - Alpha",  # "3 - Alpha" / "4 - Beta" / "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "scipy~=1.7.3",
        "matplotlib~=3.5.1",
        "numpy~=1.21.6",
    ],  # change with new version
)
