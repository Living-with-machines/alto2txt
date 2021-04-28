# Extract plain text from newspapers (extract_text 0.3.0)

Converts XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN or UKP format) publications to plaintext articles and generates minimal metadata. Downsampling can be used to convert only every Nth issue of each newspaper. One text file is output per article, each complemented by one XML metadata file.

Quality assurance is performed to check for:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

## Installation

We recommend installation via Anaconda:

* Refer to [Anaconda website and follow the instructions](https://docs.anaconda.com/anaconda/install/).

* Create a new environment for alto2txt

```bash
conda create -n py37alto python=3.7
```

* Activate the environment:

```bash
conda activate py37alto
```

* Install additional packages

```bash
pip install -r requirements.txt
```

## Usage

```
extract_publications_text.py [-h] [-d [DOWNSAMPLE]]
                                    [-p [PROCESS_TYPE]]
                                    [-l [LOG_FILE]]
                                    [-n [NUM_CORES]]
                                    xml_in_dir txt_out_dir

Converts XML publications to plaintext articles

positional arguments:
  xml_in_dir            Input directory with XML publications
  txt_out_dir           Output directory for plaintext articles

optional arguments:
  -h, --help            show this help message and exit
  -d [DOWNSAMPLE], --downsample [DOWNSAMPLE]
                        Downsample. Default 1
  -l [LOG_FILE], --log-file [LOG_FILE]
                        Log file. Default out.log
  -p [PROCESS_TYPE], --process-type [PROCESS_TYPE]
                        Process type.
                        One of: single,serial,multi,spark
                        Default: multi
  -n [NUM_CORES], --num-cores [NUM_CORES]
                        Number of cores (Spark only). Default 1")
```

`xml_in_dir` is expected to hold XML for multiple publications, in the following structure:

```
xml_in_dir
|-- publication
|   |-- year
|   |   |-- issue
|   |   |   |-- xml_content
|   |-- year
|-- publication
```

However, if `-p|--process-type single` is provided then `xml_in_dir` is expected to hold XML for a single publication, in the following structure:

```
xml_in_dir
|-- year
|   |-- issue
|   |   |-- xml_content
|-- year
```

`txt_out_dir` is created with an analogous structure to `xml_in_dir`.

`PROCESS_TYPE` can be one of:

* `single`: Process single publication.
* `serial`: Process publications serially.
* `multi`: Process publications using multiprocessing (default).
* `spark`: Process publications using Spark.

`DOWNSAMPLE` must be a positive integer, default 1.

The following XSLT files need to be in an `extract_text.xslts` module:

* `extract_text_mets18.xslt`: METS 1.8 XSL file.
* `extract_text_mets13.xslt`: METS 1.3 XSL file.
* `extract_text_bln.xslt`: BLN XSL file.
* `extract_text_ukp.xslt`: UKP XSL file.

## Process publications

Assume `~/BNA` exists and matches the structure above.

Extract text from every publication:

```bash
./extract_publications_text.py ~/BNA txt
```

Extract text from every 100th issue of every publication:

```bash
./extract_publications_text.py ~/BNA txt -d 100
```

## Process a single publication

Extract text from every issue of a single publication:

```bash
./extract_publications_text.py -p single ~/BNA/0000151 txt
```

Extract text from every 100th issue of a single publication:

```bash
./extract_publications_text.py -p single ~/BNA/0000151 txt -d 100
```

## Configure logging

By default, logs are put in `out.log`.

To specify an alternative location for logs, use the `-l` flag e.g.

```bash
./extract_publications_text.py -l mylog.txt ~/BNA txt -d 100 2> err.log
```

## Process publications via Spark

[Information on running on spark.](spark_instructions.md)

## XML metadata

Metadata about `extract_text.py` itself is inserted into the XML metadata files. The current values, including version, are defined in `extract_text_common.xslt`.

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

## Update version

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

## Future work

* Export more metadata from alto, probably by parsing mets first.
* Check and ensure that articles that span multiple pages are pulled into a single article file.
* Smarter handling of articles spanning multiple pages.
