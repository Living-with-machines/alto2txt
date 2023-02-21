# `alto2txt`: Extract plain text from digital newspaper OCR scans

*Version extract_text 0.3.4*

![GitHub](https://img.shields.io/github/license/Living-with-Machines/alto2txt) ![PyPI](https://img.shields.io/pypi/v/alto2txt) [![DOI](https://zenodo.org/badge/259340615.svg)](https://zenodo.org/badge/latestdoi/259340615)

`alto2txt` converts `XML` `ALTO`/`METS` Optical Character Recognition (OCR) scans into plaintext files with minimal metadata.

**`XML` compatibility: `METS 1.8`/`ALTO 1.4`, `METS 1.3`/`ALTO 1.4`, `BLN`, or `UKP` format**

`ALTO` and `METS` are industry standards maintained by the [US Library of Congress](https://www.loc.gov/librarians/standards) targeting newspaper digitization used by hundreds of modern, large-scale newspaper digitization projects. One text file is output per article, each complemented by one `XML` metadata file[^1] .

[`METS` (Metadata Encoding and Transmission Standard)](http://www.loc.gov/standards/mets/) is a standard for encoding descriptive, administrative, and structural metadata regarding objects within a digital library, expressed in `XML`. [`ALTO` (Analyzed Layout and Text Objects)](https://www.loc.gov/standards/alto/) is an [`XML schema`](https://en.wikipedia.org/wiki/XML_schema) for technical metadata describing the layout and content of text resources such as book or newspaper pages. `ALTO` is often used in combination with `METS` but can also be used independently. Details of the `ALTO` schema are avilable at https://github.com/altoxml/schema.


## Quick Install

### `pip`

As of verion `v0.3.4` `alto2txt` is available on [`PyPI`](https://pypi.org/project/alto2txt/) and can be installed via

```bash
pip install alto2txt
```

### `conda`

If you are comfortable with the command line, git, and already have Python & Anaconda installed, you can install `alto2txt` by navigating to an empty directory in the terminal and run the following commands:

```bash
git clone https://github.com/Living-with-machines/alto2txt.git
cd alto2txt
conda create -n py37alto python=3.7
conda activate py37alto
pip install pyproject.toml
```

[Click here](/Demo.md) for more in-depth installation instructions using demo files.

## Usage

> *Note*: the formatting below is altered for readability
```
usage: alto2txt [-h]
                [-p [PROCESS_TYPE]]
                [-l [LOG_FILE]]
                [-d [DOWNSAMPLE]]
                [-n [NUM_CORES]]
                xml_in_dir txt_out_dir

Converts XML publications to plaintext articles

positional arguments:
  xml_in_dir            Input directory with XML publications
  txt_out_dir           Output directory for plaintext articles

optional arguments:
  -h, --help            show this help message and exit
  -p [PROCESS_TYPE], --process-type [PROCESS_TYPE]
                        Process type. One of: single,serial,multi,spark Default: multi
  -l [LOG_FILE], --log-file [LOG_FILE]
                        Log file. Default out.log
  -d [DOWNSAMPLE], --downsample [DOWNSAMPLE]
                        Downsample. Default 1
  -n [NUM_CORES], --num-cores [NUM_CORES]
                        Number of cores (Spark only). Default 1")
```
To read about downsampling, logs, and using spark see [Advanced Information](advanced.md).

## Process Types


`-p | -process-type` can be one of:

* `single`: Process single publication.
* `serial`: Process publications serially.
* `multi`: Process publications using multiprocessing (default).
* `spark`: Process publications using Spark.

## Process Multiple Publications

For default settings, (`multi`) multiprocessing assumes the following directory structure for multiple publications in `xml_in_dir`:

```
xml_in_dir/
  ├── publication
  │     ├── year
  │     │     └── issue
  │     │            └── xml_content
  │     └── year
  └── publication
```
Assuming `xml_in_dir` follows this structure, run alto2txt with the following in the terminal:

```bash
alto2txt xml_in_dir txt_out_dir
```

To downsample and only process every 100th edition:

```bash
alto2txt xml_in_dir txt_out_dir -d 100
```


## Process Single Publication

[A demo for processing a single publication is available here.](Demo.md)

If `-p|--process-type single` is provided then `xml_in_dir` is expected to hold `XML` for a single publication, in the following structure:

```
xml_in_dir/
  ├── year
  │     └── issue
  │           └── xml_content
  └── year
```

Assuming `xml_in_dir` follows this structure, run `alto2txt` with the following in the terminal in the folder `xml_in_dir` is stored in:

```bash
alto2txt -p single xml_in_dir txt_out_dir
```

To downsample and only process every 100th edition from the one publication:

```bash
alto2txt -p single xml_in_dir txt_out_dir -d 100
```

## Plain Text Files Output

`txt_out_dir` is created with an analogous structure to `xml_in_dir`.
One `.txt` file and one metadata `.xml` file are produced per article.

## Quality Assurances

Quality assurance is performed to check for:

* Unexpected directories.
* Unexpected files.
* Malformed `XML`.
* Empty files.
* Files that otherwise do not expose content.

## Future work

* Export more metadata from `ALTO`, probably by parsing `METS` first.
* Check and ensure that articles that span multiple pages are pulled into a single article file.
* Smarter handling of articles spanning multiple pages.

[^1]: For a more detailed description see: https://www.coloradohistoricnewspapers.org/forum/what-is-metsalto/

> Last updated 2023-02-21
