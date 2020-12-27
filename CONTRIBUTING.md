# Contributing

## Getting Started

Make sure you have [Poetry](https://python-poetry.org) installed. After cloning
the repo, create the environment with

```bash
poetry install
```

The `Makefile` contains commands for common tasks, such as running tests
(`make test`) and linting (`make lint`).

## Documentation

With the dev requirements installed, serve the docs locally with:

```bash
make servedocs
```

To build the docs to the `site` folder, run:

```bash
make docs
```

## Deployment

To deploy, make sure the dev requirements are installed. Then run:

```bash
make release
```

Alternatively, once a version tag has been created with bump2version, push the
commit and tag with

```bash
git push
git push --tags
```

GitHub Actions will then build and deploy the appropriate versions.
