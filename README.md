# LATEX Citation Generator
This was a fast and sloppy script to generate citations from a PDF file.
Particularly useful when you have a lot of citations and you don't want to do it manually...

## Usage

A requirements.txt file is included to install the necessary packages.
You can run:

```bash
pip install -r requirements.txt
```

You can either get the links directly from the PDF (duplicates are ommited) or you can provide a file with the links.
An example of such a file can be seen in `links-shopsy.txt`.

Just run 
```bash
python generator.py --pdf <path-to-pdf> --out <path-to-output>
```
for using a PDF file, or
```bash
python generator.py --txt <path-to-txt> --out <path-to-output>
```
for using a txt file with links.

the `--out` flag is optional, the default filename is `bibliography.bib`.

## Citation style

Standard online citation style.

```latex
@misc{ref1,
  author = {},
  title = {},
  year = {},
  note = {Last accessed <current date>},
  url = {}
}
```

## Example

```bash
python generator.py --pdf phil.pdf --out bibliography.bib
```

This will generate a `bibliography.bib` file with the citations from the passed PDF.

