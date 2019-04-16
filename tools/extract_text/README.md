# Extract plain text from newspapers (extract_text v0.2.1)

Converts XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN or UKP format) publications to plaintext articles and generates minimal metadata. Downsampling can be used to convert only every Nth issue of each newspaper. One text file is output per article, each complemented by one XML metadata file.

Each publication is processed concurrently.

Quality assurance is also performed to check for:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

## Requirements

Python 2.7 (this code has not been tested under Python 3).

Python packages listed in `requirements.txt`.

## Usage

```
extract_publications_text.py [-h] [-d [DOWNSAMPLE]] [-s]
                                    xml_in_dir txt_out_dir

Converts XML publications to plaintext articles

positional arguments:
  xml_in_dir            Input directory with XML publications
  txt_out_dir           Output directory for plaintext articles

optional arguments:
  -h, --help            show this help message and exit
  -d [DOWNSAMPLE], --downsample [DOWNSAMPLE]
                        Downsample
  -s, --singleton       Specify that xml_in_dir holds XML for a single
                        publication
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

However, if `-s`|`--single` is provided then `xml_in_dir` is expected to hold XML for a single publication, in the following structure:

```
xml_in_dir
|-- year
|   |-- issue
|   |   |-- xml_content
|-- year
```

`txt_out_dir` is created with an analogous structure to `xml_in_dir`.

`DOWNSAMPLE` must be a positive integer, default 1.

The following XSLT files need to be in an `extract_text.xslts` module:

* `extract_text_mets18.xslt`: METS 1.8 XSL file.
* `extract_text_mets13.xslt`: METS 1.3 XSL file.
* `extract_text_bln.xslt`: BLN XSL file.
* `extract_text_ukp.xslt`: UKP XSL file.

## Processing many publications

Assume `~/BNA` exists and matches the structure above.

Extract text from every publication:

```bash
./extract_publications_text.py ~/BNA txt 2> err.log
```

Extract text from every 100th issue of every publication:

```bash
./extract_publications_text.py ~/BNA txt -d 100 2> err.log
```

## Processing a single publication

Extract text from every issue of a single publication:

```bash
./extract_publications_text.py -s ~/BNA/0000151 txt 2> err.log
```

Extract text from every 100th issue of a single publication:

```bash
./extract_publications_text.py -s ~/BNA/0000151 txt -d 100 2> err.log
```

While running, in another screen, run:

```
less +F err.log
```

and look for `WARN` messages.

**On completion:**

* Plaintext and XML metadat files are in `txt`.
* Logs and errors are in `err.log`.

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
