# Contributing

Contributions via [GitHub issues](https://github.com/Living-with-machines/alto2txt/issues) and [pull requests](https://github.com/Living-with-machines/alto2txt/pulls) very welcome. To install locally for contribtuions we recommend using [`poetry`](https://python-poetry.org/).

## Local checkout

1. Install [`poetry`](https://python-poetry.org/docs/#installation)
2. `git checkout https://github.com/Living-with-machines/alto2txt.git`
3. `cd alto2txt`
4. `poetry install`

## [`pre-commit`](https://pre-commit.com/) local changes

Whatever contribution you make, be it code or documentation, your changes will need to pass our [`pre-commit`](https://pre-commit.com/) [configuration](https://github.com/Living-with-machines/alto2txt/blob/main/.pre-commit-config.yaml). To prepare that:

1. Follow [installation instructions](https://pre-commit.com/#install)
2. Add `pre-commit` [git commit hooks](https://pre-commit.com/#3-install-the-git-hook-scripts)

```console
cd path/to/alto2txt
pre-commit install
```

3. Make your local commit and see if any `pre-commit` changes are added. See a [best practice guide](https://www.conventionalcommits.org/en/v1.0.0/#examples) for writing these:

```console
git commit -m "docs: correct spelling of CHANGELOG"
```

## Running tests

Once you've made any changes, please add a test within the `tests/` folder to ensure your contribution produces correct results and to ease our process of reviewing and understanding changes. Once you've written a test, you should be able to run it via

```console
poetry run pytest
```

if you need to debug your changes and/or tests, you can add

```console
poetry run pytest --pdb
```

to drop into [`ipython`](https://ipython.readthedocs.io/en/stable/) to and interactively debug tests and code. You should also see an example of [test coverage](https://coverage.readthedocs.io/en/7.1.0/) which indicates how much of the code is tested.

```console
================================= test session starts =================================
platform darwin -- Python 3.10.10, pytest-7.2.1, pluggy-1.0.0
rootdir: /Users/you-user-name/path-to-git-checkouts/alto2txt, configfile: pyproject.toml
plugins: cov-4.0.0
collected 8 items

tests/test_e2e.py ...s.ss                                                       [ 87%]
tests/test_import.py .                                                          [100%]

--------- coverage: platform darwin, python 3.10.10-final-0 ----------
Name                                        Stmts   Miss  Cover
---------------------------------------------------------------
src/alto2txt/extract_publications_text.py      21      1    95%
src/alto2txt/spark_xml_to_text.py              29     29     0%
src/alto2txt/xml_to_text.py                   111     42    62%
src/alto2txt/xml_to_text_entry.py              38      6    84%
---------------------------------------------------------------
TOTAL                                         320     78    76%

5 files skipped due to complete coverage.
```

The higher that percentage, *generally* the better. In the example above, any contributions to testing `spark_xml_to_text.py` would be very appreciated.

## Documentation with Docsify

Documentation is a collection of [`markdown`](https://www.markdownguide.org/basic-syntax/) files rendered by [`docsify`](https://docsify.js.org/
) and staticly hosted on [GitHub Pages](https://pages.github.com/). To contribute:

1. Edit the `.md` files within `docs/`.
2. Add any extra pages to `_sidebar.md` or reorder them
3. Generate an [issue](https://github.com/Living-with-machines/alto2txt/issues) describing what you've added
4. Make a [pull request](https://github.com/Living-with-machines/alto2txt/pulls)

To preview locally from the terminal:

1. Navigate to your `alto2txt` repository (and follow installation instructions above if needed).
3. `poetry shell` to activate your local `python` environment
4. `cd docs && python -m http.server 3000` to render the `docs`
5. Navigate to `http://localhost:3000` in a browser to render changes as you make them

## Update Version

Once you've made a contribution, you may need to update the `alto2txt` version number. If requested, here's an example of following that process

1. Edit `README.md`:

```md
# Extract plain text from newspapers (extract_text 0.3.0)
```

2. Edit `pyproject.toml`:

```toml
version = "0.3.4"
```

3. Exit `extract_text/xslts/extract_text_common.xslt`:

```xml
<xsl:param name="version">0.3.0</xsl:param>
```
