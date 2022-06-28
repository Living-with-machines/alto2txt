

## How to update the package version number

To update the version number:

1. Edit `README.md`:

```
# Extract plain text from newspapers (extract_text 0.3.0)
```

2. Edit `setup.py`:

```
version="0.3.0",
```

3. Exit `extract_text/xslts/extract_text_common.xslt`:

```
<xsl:param name="version">0.3.0</xsl:param>
```