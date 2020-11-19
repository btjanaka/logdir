"""Installation instructions for LogDir."""

from setuptools import setup


def readme():
    """Grabs the full text of the README."""
    with open("README.md") as file:
        return file.read()


install_requires = [
    "ruamel.yaml>0.15",
    "toml>=0.10",
    "dulwich>=0.20.0",
]

extras_require = {
    "dev": [
        "pip==20.2.4",
        "isort",
        "yapf",
        "pylint",

        # Documentation
        "mkdocs==1.1.2",
        "mkdocs-material==6.1.0",
        "mkdocstrings==0.13.6",
        "pymdown-extensions==8.0.1",
        "pygments==2.7.2",

        # Testing
        "pytest==4.6.5",
        "pytest-cov==2.10.1",
        "pytest-runner==5.1",
        "freezegun==1.0.0",

        # Distribution
        "bump2version==0.5.11",
        "wheel==0.33.6",
        "twine==1.14.0",
    ],
}

setup(
    name="logdir",
    version="0.5.0",
    author="Bryon Tjanaka",
    author_email="bryon@btjanaka.net",
    description="A utility for managing logging directories.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="http://github.com/btjanaka/logdir",
    install_requires=install_requires,
    extras_require=extras_require,
    license="MIT",
    keywords="log logging utilities",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    packages=["logdir"],
)
