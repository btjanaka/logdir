"""Installation instructions for LogDir."""

from setuptools import setup


def readme():
    """Grabs the full text of the README."""
    with open("README.md") as file:
        return file.read()


setup(
    name="logdir",
    version="0.2.2",
    author="Bryon Tjanaka",
    author_email="bryon@btjanaka.net",
    description="A utility for managing logging directories.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="http://github.com/btjanaka/logdir",
    install_requires=[],
    extras_require={},
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
