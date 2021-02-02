===================================================================
                  The manitex Package
===================================================================

Author:  Serge Rey  
Version:  0.01 (2021/01/08)  
License:  LPPL v1.3 or later (LaTeX code) and BSD 3-Clause (Python code)  
Development:  https://github.com/sjsrey/manitex
Requirements:  Python 3+

The manitext package builds a manifest of files for a Latex article that has
been accepted for publication. 

## Features

- archive of manifest in a zip file
- automatic indexing of figures and graphic files


## Using 

If the main latex document is called `main.tex`, we first need to generate a list of files required to compile the paper. To do this, add the following at the top of the main latex document:

```
\RequirePackage{snapshot}
```

Compiling the paper with `pdflatex main` will produce a file called `main.dep`
that contains information that can be used to build the manifest. The
`main.dep` file is required for `manitex` to work and an exception will be
raised if the file is missing.


### Building the manifest

```
manitex main.tex
```
Will produce the zip file `main.zip` that contains all the figures and main
tex files required to build the pdf version of the article, along with a
`README.md` file that provides an index/explanation for the copy-editor.





