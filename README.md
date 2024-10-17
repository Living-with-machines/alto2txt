# `alto2txt`: Extract plain text from digital newspaper OCR scans

![GitHub](https://img.shields.io/github/license/Living-with-Machines/alto2txt) ![PyPI](https://img.shields.io/pypi/v/alto2txt) [![DOI](https://zenodo.org/badge/259340615.svg)](https://zenodo.org/badge/latestdoi/259340615) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

*Version extract_text 0.3.4*

`alto2txt` converts `XML` `ALTO`/`METS` Optical Character Recognition (OCR) scans into plaintext files with minimal metadata.

**`XML` compatibility: `METS 1.8`/`ALTO 1.4`, `METS 1.3`/`ALTO 1.4`, `BLN`, or `UKP` format**

## [Full documentation and demo instructions.](https://living-with-machines.github.io/alto2txt/#/)

`ALTO` and `METS` are industry standards maintained by the [US Library of Congress](https://www.loc.gov/librarians/standards) targeting newspaper digitization used by hundreds of modern, large-scale newspaper digitization projects. One text file is output per article, each complemented by one `XML` metadata file[^1] .

[`METS` (Metadata Encoding and Transmission Standard)](http://www.loc.gov/standards/mets/) is a standard for encoding descriptive, administrative, and structural metadata regarding objects within a digital library, expressed in `XML`. [`ALTO` (Analyzed Layout and Text Objects)](https://www.loc.gov/standards/alto/) is an [`XML schema`](https://en.wikipedia.org/wiki/XML_schema) for technical metadata describing the layout and content of text resources such as book or newspaper pages. `ALTO` is often used in combination with `METS` but can also be used independently. Details of the `ALTO` schema are avilable at https://github.com/altoxml/schema.


## Quick Install

### `pip`

As of version `v0.3.4`, `alto2txt` is available on [`PyPI`](https://pypi.org/project/alto2txt/) and can be installed via

```console
$ pip install alto2txt
```

### `conda`

If you are comfortable with the command line, git, and already have Python & Anaconda installed, you can install `alto2txt` by navigating to an empty directory in the terminal and run the following commands:

```console
$ git clone https://github.com/Living-with-machines/alto2txt.git
$ cd alto2txt
$ conda create -n py37alto python=3.7
$ conda activate py37alto
$ pip install pyproject.toml
```

### Installation of a test release

If you need (or want) to install a test release of `alto2txt` you will likely be advised of the specific version number to install. This command will install `v0.3.1-alpha.20`:

```bash
$ pip install -i https://test.pypi.org/simple/ alto2txt==0.3.1a20
```

[Click here](https://living-with-machines.github.io/alto2txt/#Demo.md) for more in-depth installation instructions using demo files.

## Usage

> *Note*: the formatting below is altered for readability

```
$ alto2txt -h

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

To read about downsampling, logs, and using spark see [Advanced Information](https://living-with-machines.github.io/alto2txt/#/advanced).

## Process Types

`-p | -process-type` can be one of:

* `single`: Process single publication.
* `serial`: Process publications serially.
* `multi`: Process publications using multiprocessing (default).
* `spark`: Process publications using Spark.

### Process Multiple Publications

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

```console
$ alto2txt xml_in_dir txt_out_dir
```

To downsample and only process every 100th edition:

```console
$ alto2txt xml_in_dir txt_out_dir -d 100
```

### Process Single Publication

[A demo for processing a single publication is available here.](https://living-with-machines.github.io/alto2txt/#/?id=process-single-publication)

If `-p|--process-type single` is provided then `xml_in_dir` is expected to hold `XML` for a single publication, in the following structure:

```
xml_in_dir/
  ├── year
  │     └── issue
  │           └── xml_content
  └── year
```

Assuming `xml_in_dir` follows this structure, run `alto2txt` with the following in the terminal in the folder `xml_in_dir` is stored in:

```console
$ alto2txt -p single xml_in_dir txt_out_dir
```

To downsample and only process every 100th edition from the one publication:

```console
$ alto2txt -p single xml_in_dir txt_out_dir -d 100
```

### Plain Text Files Output

`txt_out_dir` is created with an analogous structure to `xml_in_dir`.
One `.txt` file and one metadata `.xml` file are produced per article.


## Configure logging

By default, logs are put in `out.log`.

To specify an alternative location for logs, use the `-l` flag e.g.

```console
$ alto2txt -l mylog.txt single xml_in_dir txt_out_dir -d 100 2> err.log
```

## Process publications via Spark

[Information on running on spark.](https://living-with-machines.github.io/alto2txt/#/advanced?id=using-spark)

## Contributing

Suggestions, code, tests, further documentation and features – especially to cover various OCR output formats – are needed and welcome. For details and examples see the [Contributing](https://living-with-machines.github.io/alto2txt/#/contributing) section.

## Future work

For a complete list of future plans see the [GitHub issues list](https://github.com/Living-with-machines/alto2txt/issues). Some highlights include:

* Export more metadata from alto, probably by parsing `mets` first.
* Check and ensure that articles that span multiple pages are pulled into a single article file.
* Smarter handling of articles spanning multiple pages.

# Copyright

## Software

Copyright 2022 The Alan Turing Institute, British Library Board, Queen Mary University of London, University of Exeter, University of East Anglia and University of Cambridge.

See [LICENSE](LICENSE) for more details.

## Example Datasets

This repo contains example datasets, which have been taken from the [British Library Research Repository](https://bl.iro.bl.uk/concern/datasets/551cdd7b-580d-472d-8efb-b7f05cf64a11) ([DOI link](https://doi.org/10.23636/1235)).

This data is "CC0 1.0 Universal Public Domain" - [No Copyright - Other Known Legal Restrictions](https://rightsstatements.org/page/NoC-OKLR/1.0/?language=en)

- There is a subset of the example data in the `demo-files` directory.
- There are adapted copies of the data in the `tests/tests/test_files` directory. These have been edited to test errors and edge cases.

# Funding and Acknowledgements

This software has been developed as part of the [Living with Machines](https://livingwithmachines.ac.uk) project.

This project, funded by the UK Research and Innovation (UKRI) Strategic Priority Fund, is a multidisciplinary collaboration delivered by the Arts and Humanities Research Council (AHRC), with The Alan Turing Institute, the British Library and the Universities of Cambridge, East Anglia, Exeter, and Queen Mary University of London. Grant reference: AH/S01179X/1

> Last updated 2023-02-21

[^1]: For a more detailed description see: https://www.coloradohistoricnewspapers.org/forum/what-is-metsalto/
