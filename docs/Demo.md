# Demo 

A working example of alto2txt. 

Input xml files from digitised newspapers create an object for every section, paragraph, sentence, and individual word, making it difficult to read articles. Each newspaper page has an associated alto (.xml) file with content, and the pages share a mets (.xml) file with meta data about what articles/other content contain and where.

The resulting .txt files are one per article, which may span multiple newspaper pages. 

## TL;DR

If you are comfortable with the command line, git, and already have Python & Anaconda installed, these are the steps to run the demo: 

Navigate to an empty directory in the terminal and run the following commands:

```
> git clone https://github.com/Living-with-machines/alto2txt.git
> cd alto2txt
> conda create -n py37alto python=3.7
> conda activate py37alto
> pip install -r requirements.txt
> ./extract_publications_text.py -p single demo-files demo-output 
```
The resulting plain text files of the articles are in `alto2txt/demo-output/`. 

Read on for a more in-depth explanation.

## Install

It is recommended to use [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) which is a data science distribution for Python and R. 

#### Download the code directory

If you are familiar with git, use the following command in a blank directory from your terminal:

```
git clone https://github.com/Living-with-machines/alto2txt.git
```

You can also download the directory as a .zip [from here.](https://github.com/Living-with-machines/alto2txt/archive/refs/heads/master.zip)

Unzip and navigate to your new copy of alto2txt folder in the terminal or the Anaconda Prompt. 

```
cd ~myFolder/alto2txt
```

#### Create Python Environment

Create a new [Conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) with Python 3.7.  The environment name can be whatever you choose, here it is `py37alto`:

```
conda create -n py37alto python=3.7
```
After creating the environment, activate it:

```
conda activate py37alto
```
#### Install Required Packages


Install the required packages which are outlined in requirements.txt:

```
pip install -r requirements.txt
```
Press `y` to confirm the installation process. You should now have all the required Python packages within your conda environment to run Alto2txt. 

## Example Alto files

You should see a subdirectory called `demo-files`. These come from a newspaper published on the 17th of February, 1824. The directory tree structure is important, and will be mirrored in the output. 

```
alto2txt/
└── demo-files/
        └── 1824/
              └── 0217/
                    ├── 0002647_18240217_0001.xml
                    ├── 0002647_18240217_0002.xml
                    ├── 0002647_18240217_0003.xml
                    ├── 0002647_18240217_0004.xml
                    └── 0002647_18240217_mets.xml
└── demo-output/
└── extract_text/
└── ...
```
Our output `.txt` files will end up in the currently empty `demo-output/` folder. 

#### Alto File Contents

There are four files with the file name ending in `_000x.xml`. These alto files contain the OCR information from the four pages scanned from the newspaper. Within each one, each word from the newspaper page has reference IDs and exists within a tree, for example:

```
0002647_18240217_0001.xml
...
<Layout>
<Page ID = "P1" ... >
    <PrintSpace ID = "P1_PS000001" ... />
        <TextBlock ID = "pa0001001" ... />
            <TextLine ID = "P1_TL000001" ... />
                <String ID = "word000001" ... CONTENT = "hello" ... /> 
```

Alto2txt will extract all these individual words and create a text file for each article. 

#### Mets File Contents

The other file in the `demo-files/` directory ends with `_mets.xml`. This contains the meta information for this newspaper edition. It contains a map of the different articles that may or may not cross multiple pages, within a structure called `<mets:structLink>`. 

Here is a short example, which defines **Article 01** as the first paragraph on page 1, and contains the `xlink:href="#pa0001001"` which is the `Textblock ID` you can see in `0002647_18240217_0001.xml` above. 

```
<mets:structLink>
    <mets:smLinkGrp>
        <mets:smLocatorLink xlink:href="#art0001" xlink:label="article" ... />
        <mets:smLocatorLink xlink:href="#pa0001001" xlink:label="page1 area1" ... />
        <mets:smArcLink xlink:type="arc" xlink:from="article" xlink:to="page1 area1" ... />
    </mets:smLinkGrp>
</mets:structLink>
```
Alto2txt will produce a `.txt` file for every Article (and other content, for example Advert) defined in this mets file. 


## Run Alto2Txt

Make sure you have navigated to the Alto2txt directory in your terminal or Anaconda prompt. For this demo, we are using a single edition for a single publication. 

``` 
./extract_publications_text.py -p single demo-files demo-output 
```

Here we use the positional argument `-p` to determine which process type, in this case `single`. The script can be run on many publications and years by default, but in this case we only have one publication. 

The next argument `demo-files` provides the input directory, and then `demo-output` provides the output directory. If you navigate to this folder you will see a directory structure that mirrors the input directory. 


## Output Text (.txt) files

Here are the newly created files:

```
alto2txt/
└── demo-output/
        └── 1824/
              └── 0217/
                    ├── 0002647_18240217_art0001_metadata.xml
                    ├── 0002647_18240217_art0001.txt
                    ├── ...
                    ├── ...
                    └── ...
```
A total of 26 articles are extracted from the alto files, and one advert. Each plain text article file has an associated `metadata.xml` file. The meta data comes from the original source mets file. 

## Further Examples

Running these steps for your own files works in the same way. Your source and/or output directory does not need to be within `/alto2txt/` as long as you put the full path name into the command arguments. 


#### Run on a single publication, multiple years, multiple editions

```
./extract_publications_text.py -p single input-directory output-directory 
```


#### Run on multiple publications, multiple years, multiple editions

```
./extract_publications_text.py input-directory output-directory 
```

#### Extract every 100th edition from every publication

```
./extract_publications_text.py input-directory output-directory -d 100 
```
Where `-d` determines the downsample value. 

#### Extract every 100th edition from one publication

```
./extract_publications_text.py -p single input-directory output-directory -d 100 
```