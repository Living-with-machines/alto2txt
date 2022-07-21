# Changelog
All notable changes to this software will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

Please maintain both this file AND the `README.md` file.

## [0.3.4]

### Added
 * Added `PyPI` version and `MIT` license badges to `README.md`
 * Added `pytest-cov` with default options to assess documentation
 * Added `isort` to `.pre-commit-config.yaml` to sort import consistency
 * Added `pycln` to  `.pre-commit-config.yaml` to check unused imports
 * Added `pycln` configuration to `pyproject.toml`
 * Added `alto2txt` as a command line script in `pyproject.toml`

### Changed
 * Switch from `Apache v2.0` license to `MIT` license, inline with project recommendations.
 * Updated `mypy` in `.pre-commit-config.yaml`

### Deprecated
 * Replace `extract_publications_text.py` with the `alto2txt` `command line interface` script specified in `pyproject.toml`

### Removed
 * `setup.py`
 * `requirements.txt`

### Fixed

 * Fixed `python = ">3.6.0"` in `pyproject.toml` rather than `>3.7` for consistency with documentation
 * Fixed licensing ambiguity (now all should be `MIT`)
 * Fixed typos in `README.md`
 * Fixed surperflous imports via `pycln` in `pre-commit`

### Security

## v0.3.3

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## v0.3.2

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## v0.3.1

### Added
 * Added this changelog file.
 * Established use of [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for this project.
 * Added a separate `CONTRIBUTING.md` doc for software developers notes.
 * Added a separate copyright notice for example datasets

### Changed

### Deprecated

### Removed

### Fixed

### Security

## v0.3.0 and before (prior to 2022-04-27)

For changes prior to the introduction of this changelog, see the [README.md file at that point in time](https://github.com/Living-with-machines/alto2txt/blob/54dc404ab60943c38d2e4c27a4e080cc24d4e8da/README.md).
