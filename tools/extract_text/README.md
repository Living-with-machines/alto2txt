# Extract plain text from newspapers

## Requirements

* xsltproc

## extractbatch

Usage: `extractbatch xml_dir txt_out_dir [downsample=1]`

Use to convert (in parallel-ish) many newspapers' worth of XML
(in alto or bl_newspaper format) to plain text alongside minimal metadata.
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
(in alto or bl_newspaper format) to plain text alongside minimal metadata.
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

e.g. from Lancashire first batch

```
../BNA/0000488/1834/1227/LAGER-1834-12-27-0004.xml:1: parser error : Document is empty

^
unable to parse ../BNA/0000488/1834/1227/LAGER-1834-12-27-0004.xml
../BNA/0000153/1890/0329/BLSD-1890-03-29-0007.xml:1499: parser error : Char 0x0 out of allowed range
						
						^
../BNA/0000153/1890/0329/BLSD-1890-03-29-0007.xml:1499: parser error : Premature end of data in tag TextLine line 1493
						
						^
../BNA/0000153/1890/0329/BLSD-1890-03-29-0007.xml:1499: parser error : Premature end of data in tag TextBlock line 69
						
						^
../BNA/0000153/1890/0329/BLSD-1890-03-29-0007.xml:1499: parser error : Premature end of data in tag PrintSpace line 57
						
						^
../BNA/0000153/1890/0329/BLSD-1890-03-29-0007.xml:1499: parser error : Premature end of data in tag Page line 52
						
						^
../BNA/0000153/1890/0329/BLSD-1890-03-29-0007.xml:1499: parser error : Premature end of data in tag Layout line 51
						
						^
../BNA/0000153/1890/0329/BLSD-1890-03-29-0007.xml:1499: parser error : Premature end of data in tag alto line 2
						
						^
unable to parse ../BNA/0000153/1890/0329/BLSD-1890-03-29-0007.xml

```

## Improvements to be made

* Do this in python, it seemed like a good idea to be moving files around in a shell script, it isn't
* Spark-ify this
* Use xml libraries to do the heavy lifting
* Use XML tech to review the doc types, looking for strings is naff
* Export more metadata from the alto, probably by parsing the mets first
* Documentation could use more detail
