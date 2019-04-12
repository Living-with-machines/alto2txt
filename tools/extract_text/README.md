# Extract plain text from newspapers

## extract_text v0.2.1

### Requirements

* xsltproc
* GNU parallel
* GNU find

### extractbatch

Usage: `extractbatch xml_dir txt_out_dir [downsample=1]`

Use to convert (in parallel-ish) many newspapers' worth of XML
(in alto or bln format) to plain text alongside minimal metadata.
Downsample can be used to do every nth issue. One article per txt file.

Expected structure:
```
xml_dir
├── newspaper_id
│   ├── year
│   │   ├── issue
│   │   │   ├── xml_content
├── newspaper_id
```

This tool will also perform quality assurance on:
- unexpected directories
- unexpected files
- un well-formed xml
- empty files
- files that otherwise do not expose content

`extractbatch` uses `extracttext` to do the hard work...

### extracttext

Usage: `extracttext publication_dir txt_out_dir [downsample=1]`

Use to convert a single newspaper's worth of XML
(in alto or bln format) to plain text alongside minimal metadata.
Downsample can be used to do every nth issue. One article per txt file.

Expected structure:
```
publication_dir
├── year
│   ├── issue
│   │   ├── xml_content
├── year
```

This tool will also perform quality assurance on:
- unexpected directories
- unexpected files
- un well-formed xml
- empty files
- files that otherwise do not expose content

`extracttext` uses `extracttext.xslt` to do the transform

### Example

Assume `BNA` exists and matches the structure above

`./extractbatch ../BNA txt 100 > out 2> err` for every 100th issue
`./extractbatch ../BNA txt > out 2> err` for every issue

Optional, in another screen (while running) `less +F out` look for 'WARN'. BTW - parallel will cause output to be lumpy, as each process finishes and flushes into stdout.

see results in `txt`

review output in `err`

### Improvements to be made

* Do this in python, it seemed like a good idea to be moving files around in a shell script, it isn't
* Spark-ify this
* Use XML libraries to do the heavy lifting
* Use XML tech to review the doc types, looking for strings is naff
* Export more metadata from the alto, probably by parsing the mets first
* Documentation could use more detail

---

## extract_text.py

A Python version of the `extracttext` script.

### Requirements

See `requirements.txt`.

### Usage

```
usage: extract_text.py [-h] [-d [DOWNSAMPLE]]
                       publication_dir txt_out_dir

Extract plaintext articles from newspaper XML

positional arguments:
  publication_dir       Publication directory with XML
  txt_out_dir           Output directory with plaintext

optional arguments:
  -h, --help            show this help message and exit
  -d [DOWNSAMPLE], --downsample [DOWNSAMPLE]
                        Downsample
```

Convert a single newspaper's XML (in METS 1.8/ALTO 1.4, METS 1.3/ALTO
1.4, BLN or UKP format) to plaintext articles and generate minimal
metadata. Downsampling can be used to convert only every Nth issue of
the newspaper. One text file is output per article.

Quality assurance will also be performed to check:

* Unexpected directories.
* Unexpected files.
* Malformed XML.
* Empty files.
* Files that otherwise do not expose content.

`publication_dir` is expected to have structure:

```
publication_dir
|-- year
|   |-- issue
|   |   |-- xml_content
|-- year
```

`txt_out_dir` is created with an analogous structure.

`DOWNSAMPLE` must be a positive integer, default 1.

The following XSLT files need to be in the current directory:

* extract_text_mets18.xslt: METS 1.8 XSL file.
* extract_text_mets13.xslt: METS 1.3 XSL file.
* extract_text_bln.xslt: BLN XSL file.
* extract_text_ukp.xslt: UKP XSL file.

### Examples

Assume `~/BNA/0000151` exists and matches the structure above.

Extract text from every issue:

```bash
./extract_publication_text.py ~/BNA/0000151 txt > out.log 2> err.log
```

Extract text from every 100th issue:

```bash
./extract_publication_text.py ~/BNA/0000151 txt -d 100 > out.log 2> err.log
```

While running, in another screen, run:

```
less +F out.log
```

and look for `WARN` messages.

On completion:

* Plaintext and XML metadat files are in `txt`.
* Logs are in `out.log`.
* Errors are in `err.log`.
