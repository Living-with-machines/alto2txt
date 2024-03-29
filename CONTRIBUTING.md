
## Coding standards

The following standards are enforced via automated tests;

### Pre-commit

`pre-commit` hooks are used to ensure:

- The code is formatted according to `black` and `pep8` rules.
- White space at the end of lines is removed.
- Files end with a single blank line.
- XML and YAML files are properly formatted. If there is a need to add a malformatted file (eg for test purposes) it is possible to add an exception to these rules using an `exclude` clause in the `.pre-commit-config.yml` file.
- Where type hints are used they are correct. The use of type hints is not required.

Currently, import sort order is _not_ enforced.

### CI

- Unit and integration tests are run using `pytest`.
- `flake8` is used to test for function complexity, but only warnings (not errors) are returned.

## How to update the package version number

### To update the version number:

1. Edit `README.md`:

The document title is in the form:

```
# Extract plain text from newspapers (extract_text v0.3.1)
```

2. Use poetry to increase the version number:

For details see [the poetry documentation](https://python-poetry.org/docs/cli/#version). An example command is:

```
poetry version patch
```

1. Edit the version number in `extract_text/xslts/extract_text_common.xslt`:

```
<xsl:param name="version">0.3.1</xsl:param>
```

### To release a new version

From the `main` branch.

```bash
git checkout main
git tag -a v`poetry version -s` -m \'alto2txt release v`poetry version -s`\'
git push --tags
```

GitHub Actions will detect the tagged commit and publish the package to PyPI accordingly.

Immediately afterwards, increase the version number of the package within the code.

```bash
poetry version patch
git commit -m "Bump version number"
git push
```

This will ensure that development builds, from non-tagged commits, will be published to [TestPyPI](https://test.pypi.org/) as an `alpha` release of the next version. For example, if the latest version on PyPI is `v1.2.3`, the next development build on TestPyPI will be `v1.2.4-alphaX` (sequentially after the latest version).
