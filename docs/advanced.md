# Further Information


## `XSTL`: `XML` Stylesheet

`XSLT` (eXtensible Stylesheet Language Transformations) is the recommended style sheet language for `XML`.
The following `XSLT` files need to be in an `extract_text.xslts` module:

* `extract_text_mets18.xslt`: METS 1.8 XSL file.
* `extract_text_mets13.xslt`: METS 1.3 XSL file.
* `extract_text_bln.xslt`: BLN `XSL` file.
* `extract_text_ukp.xslt`: UKP `XSL` file.


## `XML` metadata

Metadata about `extract_text.py` itself is inserted into the `XML` metadata files.
The current values, including version, are defined in `extract_text_common.xslt`.

The following metadata for the following dataset types are **not** output, due to it not being present in the `XML` for those datasets:

METS1.3/ALTO1.4:

* `/lwm/publication/location`

BLN:

* `/lwm/process/namespace`
* `/lwm/publication/issue/item/item_type`

UKP:

* `/lwm/process/software`
* `/lwm/process/namespace`
* `/lwm/publication/title`
* `/lwm/publication/location`


## Configure Logging

By default, logs are put in `out.log`.

To specify an alternative location for logs, use the `-l` flag e.g.

```bash
alto2txt -l mylog.txt ~/xml_in_dir ~/txt_out_dir -d 100 2> err.log
```

## Using Spark

When running via Spark ensure that:

* `xml_in_dir` and `txt_out_dir` are on a file system accessible to all Spark worker nodes.
* Provide a log file location, using the `-l` flag, that is accessible to all Spark worker nodes.
* The code is available as a package on all Spark worker nodes.

For example, the code can be run on Urika requesting as follows...

Install the code as a package:

```bash
python setup.py install
```

Run `spark-submit`:

```bash
spark-submit ./extract_publications_text.py \
    -p spark \
    -n 144 \
    -l /mnt/lustre/at003/at003/<username>/log.out     \
    /mnt/lustre/at003/at003/shared/findmypast/BNA/    \
    /mnt/lustre/at003/at003/<username>/fmp-lancs-txt
```

For Urika, it is recommended that the value of 144 be used for
`NUM_CORES`. This, with the number of cores per node, determines the
number of workers/executors and nodes. As Urika has 36 cores per node,
this would request 144/36 = 4 workers/executors and nodes.


## Update Version

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

## Documentation with Docsify

Documentation exists as a static site hosted on Github Pages. Instructions can be found here: https://docsify.js.org/

1. Edit the `.md` files within `docs/`.
2. Add any extra pages to `_sidebar.md` or reorder them
3. Make sure you have a local `python` install, and we recommend via [`poetry`](https://python-poetry.org/docs/#installation)

To preview locally from the terminal:

1. Navigate to your `alto2txt` repository checkout
2. `poetry shell` to activate your local `python` environment
3. `cd docs && python -m http.server 3000` to render the `docs`
4. Navigate to `http://localhost:3000` in a browser to render changes as you make them
