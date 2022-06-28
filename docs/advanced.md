# Further Information


## XSTL: XML Stylesheet

XSLT (eXtensible Stylesheet Language Transformations) is the recommended style sheet language for XML.
The following XSLT files need to be in an `extract_text.xslts` module:

* `extract_text_mets18.xslt`: METS 1.8 XSL file.
* `extract_text_mets13.xslt`: METS 1.3 XSL file.
* `extract_text_bln.xslt`: BLN XSL file.
* `extract_text_ukp.xslt`: UKP XSL file.


## XML metadata

Metadata about `extract_text.py` itself is inserted into the XML metadata files.
The current values, including version, are defined in `extract_text_common.xslt`.

The following metadata for the following dataset types are **not** output, due to it not being present in the XML for those datasets:

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
./extract_publications_text.py -l mylog.txt ~/xml_in_dir ~/txt_out_dir -d 100 2> err.log
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
