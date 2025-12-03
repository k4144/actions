[![License](https://img.shields.io/github/license/k4144/actions)](https://github.com/k4144/actions/blob/main/LICENSE)
[![CI](https://github.com/k4144/actions/workflows/project-ci.yml/badge.svg)](https://github.com/k4144/actions/workflows/project-ci.yml)
[![Tests](./badges/tests.svg)](https://docs.pytest.org/en/stable/)
[![Coverage](./badges/coverage.svg)](https://docs.pytest.org/en/stable/)
[![Bandit](./badges/bandit.svg)](https://bandit.readthedocs.io/en/latest/)
[![Black](./badges/black.svg)](https://pypi.org/project/black/)
[![Ruff](./badges/ruff.svg)](https://pypi.org/project/ruff/)
[![Docs](./badges/docs.svg)](https://www.sphinx-doc.org/en/master/usage/quickstart.html)

# Actions & Reusable Workflows

This repository provides reusable GitHub Actions workflows designed to standardize and simplify CI/CD processes for Python projects.

## Workflows

### `project-ci`

The `project-ci` workflow is a comprehensive pipeline for Python packages. It handles:

- **Testing**: Runs `pytest` with coverage reporting.
- **Linting & Formatting**: Checks code quality using `ruff` and `black`.
- **Security Checks**: Scans for vulnerabilities using `bandit`.
- **Documentation**: Builds documentation using `sphinx`.
- **Badges**: Automatically generates and updates status badges for tests, coverage, and linting results.

- **Publishing**: the pypi publishing step has been moved into ci.yml because pypi does not support publishing from reusable workflows. this step is optional and can be disabled by removing the `publish-on` input.

## Usage

You can use the `ci.yml` file in this repository as a template for your own projects.

To use the `project-ci` workflow, add a file to your repository (e.g., `.github/workflows/ci.yml`) with the following content:

```yaml
name: CI

on: [push, pull_request, workflow_dispatch]

permissions:
  contents: write
  id-token: write

jobs:
  ci:
    uses: k4144/actions/.github/workflows/project-ci.yml@main
    with:
      python-version: "3.11"
      package-name: "your_package_name"
      # publish-on: "main" # Optional: Define branch for publishing
    secrets:
      #pypi-token: ${{ secrets.PYPI_TOKEN }}
  publish:
    needs: ci
    if: needs.ci.outputs.should_publish == 'true'
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      contents: read
      id-token: write
    steps:
      - name: Download distribution artifact
        uses: actions/download-artifact@v4
        with:
          name: ${{ needs.ci.outputs.dist_artifact }}
          path: dist

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          packages-dir: dist/
```
