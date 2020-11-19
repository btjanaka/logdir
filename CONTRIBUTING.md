# Contributing

## Getting Started

After cloning the repo, install the development dependencies with:

```bash
pip install -e .[dev]
```

## Documentation

With the dev requirements installed, serve the docs locally with:

```bash
mkdocs serve
```

To build the docs to the `site` folder, run:

```bash
mkdocs build
```

## Deployment

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
