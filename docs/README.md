# Alto2txt: Extract plain text from digitised newspapers

*Version extract_text 0.3.0*

Alto2txt converts XML publications to plaintext articles with minimal metadata.
ALTO and METS is the current industry standard for newspaper digitization used by hundreds of modern, large-scale newspaper digitization projects.
One text file is output per article, each complemented by one XML metadata file.

**XML compatibility: METS 1.8/ALTO 1.4, METS 1.3/ALTO 1.4, BLN, or UKP format**

## Usage


```
extract_publications_text.py [-h [HELP]]
                             [-d [DOWNSAMPLE]]
                             [-p [PROCESS_TYPE]]
                             [-l [LOG_FILE]]
                             [-n [NUM_CORES]]
                             xml_in_dir txt_out_dir

Converts XML publications to plaintext articles

positional arguments:
  xml_in_dir            Input directory with XML publications
  txt_out_dir           Output directory for plaintext articles

optional arguments:
  -h, --help            Show this help message and exit
  -d, --downsample      Downsample, process every [integer] nth edition.  Default 1
  -l, --log-file        Log file. Default out.log
  -p, --process-type    Process type.
                        One of: single,serial,multi,spark
                        Default: multi
  -n, --num-cores       Number of cores (Spark only). Default 1
```
To read about downsampling, logs, and using spark see [Advanced Information](advanced.md).


## Quick Install

If you are comfortable with the command line, git, and already have Python & Anaconda installed, you can install Alto2txt by navigating to an empty directory in the terminal and run the following commands:

```
> git clone https://github.com/Living-with-machines/alto2txt.git
> cd alto2txt
> conda create -n py37alto python=3.7
> conda activate py37alto
> pip install -r requirements.txt
```

[Click here](/Demo.md) for more in-depth installation instructions using demo files.


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
./extract_publications_text.py ~/xml_in_dir ~/txt_out_dir
```

To downsample and only process every 100th edition:

```bash
./extract_publications_text.py ~/xml_in_dir ~/txt_out_dir -d 100
```


## Process Single Publication

[A demo for processing a single publication is available here.](Demo.md)

If `-p|--process-type single` is provided then `xml_in_dir` is expected to hold XML for a single publication, in the following structure:

```
xml_in_dir/
  ├── year
  │     └── issue
  │           └── xml_content
  └── year
```

Assuming `xml_in_dir` follows this structure, run alto2txt with the following in the terminal:

```bash
./extract_publications_text.py -p single ~/xml_in_dir ~/txt_out_dir
```

To downsample and only process every 100th edition from the one publication:

```bash
./extract_publications_text.py -p single ~/xml_in_dir ~/txt_out_dir -d 100
```

## Plain Text Files Output

`txt_out_dir` is created with an analogous structure to `xml_in_dir`.
One `.txt` file and one metadata `.xml` file are produced per article.

## Quality Assurances

Quality assurance is performed to check for:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

## Future work

* Export more metadata from ALTO, probably by parsing METS first.
* Check and ensure that articles that span multiple pages are pulled into a single article file.
* Smarter handling of articles spanning multiple pages.


> Last updated 2022-05-24
