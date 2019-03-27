# extract_text v0.2.1
# Extract plain text from newspapers

## Requirements

* xsltproc
* GNU parallel
* GNU find

## extractbatch

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

## extracttext

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

## Example

Assume `BNA` exists and matches the structure above

`./extractbatch ../BNA txt 100 > out 2> err` for every 100th issue
`./extractbatch ../BNA txt > out 2> err` for every issue

Optional, in another screen (while running) `less +F out` look for 'WARN'. BTW - parallel will cause output to be lumpy, as each process finishes and flushes into stdout.

see results in `txt`

review output in `err`

## Improvements to be made

* Do this in python, it seemed like a good idea to be moving files around in a shell script, it isn't
* Spark-ify this
* Use XML libraries to do the heavy lifting
* Use XML tech to review the doc types, looking for strings is naff
* Export more metadata from the alto, probably by parsing the mets first
* Documentation could use more detail
