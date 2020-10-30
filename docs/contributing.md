# Contributing

## Documentation

Make sure the requirements in `requirements_dev.txt` are installed. Then, serve
the docs locally with:

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
