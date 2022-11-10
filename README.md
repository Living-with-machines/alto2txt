# `alto2txt`: Extract plain text from newspapers

![GitHub](https://img.shields.io/github/license/Living-with-Machines/alto2txt) ![PyPI](https://img.shields.io/pypi/v/alto2txt)

Converts `XML` (in `METS` `1.8`/`ALTO` `1.4`, `METS` `1.3`/`ALTO` `1.4`, `BLN` or `UKP` format) publications to plaintext articles and generates minimal metadata.


## [Full documentation and demo instructions.](https://living-with-machines.github.io/alto2txt/#/)


## Installation

### Installation using an Anaconda environment

We recommend installation via Anaconda:

* Refer to the [Anaconda website and follow the instructions](https://docs.anaconda.com/anaconda/install/).

* Create a new environment for `alto2txt`

```bash
conda create -n py37alto python=3.7
```

* Activate the environment:

```bash
conda activate py37alto
```

* Install `alto2txt` itself

Install `alto2txt` using pip:

```bash
pip install alto2txt
```

(For now it is still necessary to install using `pip`. In due course we plan to make `alto2txt` available through a `conda` channel, meaning that it can be installed directly using `conda` commands.)

### Installation using pip, outside an Anaconda environment

Note, the use of ``alto2txt`` outside a conda environment has not been as extensively tested as within a conda environment. Whilst we believe that this should work, please use with caution.

```bash
pip install alto2txt
```

### Installation of a test release

If you need (or want) to install a test release of `alto2txt` you will likely be advised of the specific version number to install. This examaple command will install `v0.3.1-alpha.20`:

```bash
pip install -i https://test.pypi.org/simple/ alto2txt==0.3.1a20
```

## Usage

Downsampling can be used to convert only every Nth issue of each newspaper. One text file is output per article, each complemented by one `XML` metadata file.



```
usage: alto2txt [-h] [-p [PROCESS_TYPE]] [-l [LOG_FILE]] [-d [DOWNSAMPLE]] [-n [NUM_CORES]]
                xml_in_dir txt_out_dir
alto2txt [-h] [-p [PROCESS_TYPE]] [-l [LOG_FILE]] [-d [DOWNSAMPLE]] [-n [NUM_CORES]]
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

`xml_in_dir` is expected to hold `XML` for multiple publications, in the following structure:

```
xml_in_dir
|-- publication
|   |-- year
|   |   |-- issue
|   |   |   |-- xml_content
|   |-- year
|-- publication
```

However, if `-p|--process-type single` is provided then `xml_in_dir` is expected to hold `XML` for a single publication, in the following structure:

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

The following `XSLT` files need to be in an `extract_text.xslts` module:

* `extract_text_mets18.xslt`: `METS 1.8 XSL` file.
* `extract_text_mets13.xslt`: `METS 1.3 XSL` file.
* `extract_text_bln.xslt`: `BLN XSL` file.
* `extract_text_ukp.xslt`: `UKP XSL` file.

## Process publications

Assume folder `BNA` exists and matches the structure above.

Extract text from every publication:

```bash
alto2txt BNA txt
```

Extract text from every 100th issue of every publication:

```bash
alto2txt BNA txt -d 100
```

## Process a single publication

Extract text from every issue of a single publication:

```bash
alto2txt -p single BNA/0000151 txt
```

Extract text from every 100th issue of a single publication:

```bash
alto2txt -p single BNA/0000151 txt -d 100
```

## Configure logging

By default, logs are put in `out.log`.

To specify an alternative location for logs, use the `-l` flag e.g.

```bash
alto2txt -l mylog.txt BNA txt -d 100 2> err.log
```

## Process publications via Spark

[Information on running on spark.](spark_instructions.md)


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

This project, funded by the UK Research and Innovation (UKRI) Strategic Priority Fund, is a multidisciplinary collaboration delivered by the Arts and Humanities Research Council (AHRC), with The Alan Turing Institute, the British Library and the Universities of Cambridge, East Anglia, Exeter, and Queen Mary University of London.
