import bibtexparser
import bibtexparser.middlewares as m
from os import path
import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json

layers = [
    m.SeparateCoAuthors(True), # Co-authors should be separated as list of strings
]

def save_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# def create_training_data(entries):
#     patterns = []
#     d = open('./dados/textosF.txt', 'a', encoding="utf-8")

#     for entry in entries:
#         filename = entry['title'].split("-")
#         pathF = './entidade/' + filename[0].strip() + '.txt'

#         if(path.exists(pathF)):
#             f = open(pathF, 'r', encoding="utf-8")

#             if hasattr(entry, 'keywords'):
#                 keywords = entry['keywords']
#             else: 
#                 keywords = ''

#             pattern = {
#                 "file": filename[0].strip() + '.txt',
#                 "title": entry['title'], 
#                 "doi": entry['doi'],
#                 "author": entry['author'],
#                 "keywords": keywords,
#                 "content": f.read()
#             }
#             patterns.append(pattern)
#         else:
#             #para consertar os arquivos que faltarem na mão
#             d.write(filename[0].strip() + '.txt' + ' ---->' + entry['title'] + '\n')

#     d.close()
#     return (patterns)

with open("bibtex/sciencedirect.bib", encoding='utf-8') as bibtex_file:
    tmp = bibtex_file.read()
    library = bibtexparser.parse_string(tmp, append_middleware=layers)

d = open('./dados/textosF.txt', 'w', encoding="utf-8")
d.write('')

def test_model(model, text):
    doc = nlp(text)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_))
    if len(entities) > 0:
        results = [text, {"entities": entities}]
        return (results)



def create_training_data(entry, text, type):
    # pattern = []

    doc = nlp(text)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_))
    if len(entities) > 0:
        results = [text, {"entities": entities}]
        return (results)
    
        
    # return (pattern)

title_data = []
doi_data = []
author_data = []

for entry in library.entries:
    filename = entry['title'].split("-")
    pathF = './entidade/' + filename[0].strip() + '.txt'

    if(path.exists(pathF)):
            f = open(pathF, 'r', encoding="utf-8")

            if hasattr(entry, 'keywords'):
                keywords = entry['keywords']
            else: 
                keywords = ''

            title = create_training_data(entry['title'], f.read(), 'TITLE')
            doi = create_training_data(entry['doi'], f.read(), 'DOI')
            author = create_training_data(entry['author'], f.read(), 'AUTHOR')

            # pattern = {
            #     "file": filename[0].strip() + '.txt',
            #     "title": entry['title'], 
            #     "doi": entry['doi'],
            #     "author": entry['author'],
            #     "keywords": keywords,
            #     "content": f.read()
            # }

            title_data.append(title)
            doi_data.append(doi)
            author_data.append(author)
    else:
        #para consertar os arquivos que faltarem na mão
        d.write(filename[0].strip() + '.txt' + ' ---->' + entry['title'] + '\n')
d.close()

# def generate_rules(patterns):
#     nlp = English()
#     ruler = EntityRuler(nlp)
#     ruler.add_patterns(patterns)
#     nlp.add_pipe(ruler)
#     nlp.to_disk("articles_ner")

# nlp = spacy.load("articles_ner")
