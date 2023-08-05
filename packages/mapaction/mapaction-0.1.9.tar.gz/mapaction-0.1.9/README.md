<p align="center">
  <a href="https://mapaction.org/">
      <img alt="MapAction" src="https://qb19onvfjt-flywheel.netdna-ssl.com/wp-content/themes/mapaction/images/logo.svg" width="210" />
  </a>
</p>
<h1 align="center">
MapAction CLI
</h1>

CLI tool for managing MapAction tasks.

## Getting Started

Requirements:

- [Poetry](https://python-poetry.org/)

### Development

```bash
poetry shell
poetry install
pre-commit install
python -m mapaction -v
```

### Build

```bash
poetry shell
poetry build
```

### Generate requirements.txt

```bash
poetry shell
poetry export -f requirements.txt --output requirements.txt
```

### Creating a release

```bash
poetry shell
poetry version <patch, minor, major>
git commit -m "Release v<Version>"
// After Merge
git tag -a v<Version> -m "release v<Version>"
```
