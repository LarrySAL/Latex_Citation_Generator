from bs4 import BeautifulSoup
import requests
from datetime import datetime
import fitz  # PyMuPDF

def get_citations(url):
    # Send GET request to URL
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return {
            'author': "",
            'title': "", 
            'year': ""
        }

    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize variables
    author = ""
    title = "" 
    year = ""

    # Try to find author - look in common metadata tags
    author_meta = soup.find('meta', {'name': ['author', 'article:author']})
    if author_meta:
        author = author_meta.get('content')
    
    # If no author found, look for company/site name
    if not author:
        company_meta = soup.find('meta', {'property': ['og:site_name', 'publisher']})
        if company_meta:
            author = company_meta.get('content')
    if author:
        author = author.replace('.', ' ').replace('_', ' ')
        words = [word.capitalize() for word in author.split()]
        author = ' '.join(words)

    # Try to find title
    title_meta = soup.find('meta', {'property': 'og:title'}) or soup.find('title')
    if title_meta:
        title = title_meta.get('content') if title_meta.get('content') else title_meta.text

    # Try to find year - look in publish date metadata
    date_meta = soup.find('meta', {'property': ['article:published_time', 'datePublished']})
    if date_meta:
        date_str = date_meta.get('content')
        try:
            year = date_str.split('-')[0]  # Extract year from ISO date format
        except:
            year = ""

    return {
        'author': author,
        'title': title, 
        'year': year
    }

def write_bibtex(file, data, url):

    for key in data:
        if data[key] is None:
            data[key] = ""

    with open(file, 'r') as f:
        first_line = f.readline().strip()
        ref_num = 1
        if first_line.startswith('#'):
            try:
                ref_num = int(first_line[1:]) + 1
            except ValueError:
                ref_num = 1
    
    with open(file, 'r+') as f:
        lines = f.readlines()[1:]
        content = ''.join(lines)
        f.seek(0)
        f.write(f"#{ref_num}\n{content}")
        f.write(f"@misc{{ref{ref_num},\n")
        f.write(f"  author = {{{data['author']}}},\n")
        f.write(f"  title = {{{data['title']}}},\n") 
        f.write(f"  year = {{{data['year']}}},\n")
        f.write(f"  note = {{Last accessed {datetime.now().strftime('%d.%b.%Y')}}},\n")
        f.write(f"  url = {{{url}}}\n")
        f.write("}\n\n")

def get_links_from_pdf(file):
    # Open the PDF file
    doc = fitz.open(file)

    # Extract links
    links = []
    for page_num in range(1, len(doc)):
        page = doc[page_num]
        for link in page.get_links():
            if "uri" in link:
                # avoid dups
                if link["uri"] in links:
                    continue
                links.append(link["uri"].strip().replace('\n', ''))

    return links

def read_links(file):
    with open(file, 'r') as f:
        links = [line.strip().replace('\n', '') for line in f.readlines()]
        return links