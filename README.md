# logdir

![Test and Deploy](https://github.com/btjanaka/logdir/workflows/Test%20and%20Deploy/badge.svg?branch=master)

A utility for managing logging directories.

<!-- vim-markdown-toc GFM -->

* [Installation](#installation)
* [Usage](#usage)
* [Examples](#examples)
* [Deployment Notes](#deployment-notes)

<!-- vim-markdown-toc -->

## Installation

To install from PyPI, run:

```bash
pip install logdir
```

To install from source,

```bash
pip install -e .
```

## Usage

## Examples

## Deployment Notes

To deploy, make sure the dev requirements are installed. Then run:

```bash
make release
```

Alternatively, once a version tag has been created with bump2version, push the
tag with

```bash
git push --tags
```

GitHub Actions will then build and deploy the appropriate versions.
