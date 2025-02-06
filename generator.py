import os
import argparse
from functions import get_links_from_pdf, get_citations, write_bibtex, read_links

parser = argparse.ArgumentParser()
parser.add_argument("--pdf", type=str, help="Path to the PDF file")
parser.add_argument("--txt", type=str, help="Path to the file with the links")
parser.add_argument("--out", type=str, default="bibliography.bib", help="Path to the output file")
args = parser.parse_args()

if args.pdf:
    links = get_links_from_pdf(args.pdf)
else:
    links = read_links(args.txt)

if not os.path.exists(args.out):
    print(f"Creating {args.out}...")
    with open(args.out, 'w') as f:
        pass

for link in links:
    data = get_citations(link)
    write_bibtex(args.out, data, link)

print("Done!")