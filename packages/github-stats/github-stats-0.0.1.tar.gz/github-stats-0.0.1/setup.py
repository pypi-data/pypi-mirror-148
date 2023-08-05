import os

from setuptools import find_packages, setup


def read(rel_path: str) -> str:
    """
    Return the contents of the file at relative path ``rel_path``.

    Args:
        rel_path: The relative path to the file.

    Returns: The contents of the file.

    """

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), "r", encoding="utf-8") as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    """
    Return the version string of the package.

    Args:
        rel_path: The relative path to the file.

    Returns: The version string.

    """

    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


long_description = read("README.md")

setup(
    name="github-stats",
    url="https://github.com/saiyalamarty/github-stats",
    version=get_version("src/github_stats/__init__.py"),
    description="Command line tool to get number of PRs reviewed by a user",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sai Yalamarty",
    author_email="sai1494@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "click",
        "pandas",
        "PyGithub",
        "rich",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "gitstats=github_stats.app:main",
        ],
    },
)
