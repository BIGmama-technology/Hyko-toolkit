<!-- x-release-please-start-version -->
 ![Static Badge](https://img.shields.io/badge/Release-v2.0.0-/?style=flat&logo=track)
<!-- x-release-please-end -->

# Hyko toolkit

A collection of functions, APIs and AI models that are available on Hyko.

## Getting Started
### Requirements
- [Poetry](https://python-poetry.org/docs/#installation)
- [Pyenv](https://github.com/pyenv/pyenv)

1. Clone the Github repository

```bash
git clone git@github.com:BIGmama-technology/Hyko-toolkit.git toolkit
```
2. Change directory into the cloned repo

```bash
cd toolkit
```
3. Copy the `.env.example` file to `.env`

```bash
cp .env.example .env
```

> Make sure to put the right values in the `.env` file.

4. Setup the toolkit locally

```bash
make setup
```

## To Build 
`./scripts/sdk_builder.py` allows you to deploy tools to hyko.

```bash
make build dir=path/to/dir host=hyko.ai 
```
