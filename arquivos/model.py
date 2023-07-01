import bibtexparser
import bibtexparser.middlewares as m

layers = [
    m.SeparateCoAuthors(True), # Co-authors should be separated as list of strings
]

with open("bibtex/sciencedirect.bib", encoding='utf-8') as bibtex_file:
    tmp = bibtex_file.read()
    library = bibtexparser.parse_string(tmp, append_middleware=layers)

print(len(library.entries))

# for entry in library.entries:
#     print(entry['journal'])
#     print(entry['title'])
#     print(entry['doi'])
#     print(entry['author'])
#     print(entry['keywords'])
#     print(entry['abstract'])
