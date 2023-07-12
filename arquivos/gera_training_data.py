import bibtexparser
import bibtexparser.middlewares as m
from os import path
import spacy
import pandas as pd
import json
import json
from datetime import datetime
from tqdm import tqdm
import regex as re

layers = [
    m.SeparateCoAuthors(True), # Co-authors should be separated as list of strings
]

# salva num json
def save_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False,indent=4)

# # abre arquivo com os bibtexs
# with open("bibtex/sciencedirect.bib", encoding='utf-8') as bibtex_file:
#     tmp = bibtex_file.read()
#     library = bibtexparser.parse_string(tmp, append_middleware=layers)

# abre arquivo com os bibtexs
with open("bibtex/portugues2.bib", encoding='utf-8') as bibtex_file:
    tmp = bibtex_file.read()
    library = bibtexparser.parse_string(tmp, append_middleware=layers)

# abre arquivo de log de textos faltantes
d = open('./dados/textosF.txt', 'w', encoding="utf-8")
d.write('')

def structure_training_data(text, kw_list, eType):
    results = []
    entities = []

    # search for instances of keywords within the text (ignoring letter case)
    for kw in tqdm(kw_list):
        # print('\n',kw)
        search = re.finditer(kw, text, flags=re.IGNORECASE)
        all_instances = [[m.start(),m.end()] for m in search]
        # print(all_instances) 
        
        # if the callable_iterator found matches, create an 'entities' list
        if len(all_instances)>0:
            for i in all_instances:
                start = i[0]
                end = i[1]
                entities.append((start, end, eType))
        # alert when no matches are found given the user inputs
        else:
            print("No pattern matches found. Keyword:", kw)
                
    # add any found entities into a JSON format within collective_dict
    if len(entities)>0:
        results = [text, {"entities": entities}]
        return results

#função que cria as listas com entidades 
def create_training_data(entry, text, eType):
    obj = []
    if(eType != "AUTHOR"): 
        obj.append(entry)
    else: 
        for author in entry:
            if(',' in author):
                tmpAuthor = author.split(',')
                author_tmp = (tmpAuthor[1] + ' ' + tmpAuthor[0])
                obj.append(re.sub('[^0-9a-zA-Z -]+', '', author_tmp))
            else:
                obj.append(re.sub('[^0-9a-zA-Z -]+', '', author))

    return structure_training_data(text, obj, eType)

#inicializa listas de treino
title_dict = {'TRAINING_DATA': []}
doi_dict = {'TRAINING_DATA': []}
author_dict = {'TRAINING_DATA': []}
cont = 0

for entry in library.entries:
    # print(entry['title'])
    tmp_file = entry['title'].replace(':','-')
    filename = tmp_file.split("-")
    pathF = './entidade/' + filename[0].strip() + '.txt'

    if(path.exists(pathF)):
            f = open(pathF, 'r', encoding="utf-8")

            if hasattr(entry, 'keywords'):
                keywords = entry['keywords']
            else: 
                keywords = ''
            
            # >>NESSE CASO ESPECÍFICO<< como estou pegando apenas informações do começo dos artigos irei limitar o tamanho do texto para facilitar o tratamento
            text_tmp = f.read()
            text = text_tmp[:10000]

            # print para checar andamento da conversão
            # print(text)
            cont+=1
            # print(entry['doi'])

            if(entry['title'] != ''): title = create_training_data(entry['title'], text, 'TITLE')
            
            if(entry['doi'] != ''): 
                if 'https://doi.org/' in entry['doi']:
                    obj = entry['doi'].split('https://doi.org/')
                    doi = create_training_data(obj[1], text, 'DOI')
                else: doi = create_training_data(entry['doi'], text, 'DOI')
                doi_dict['TRAINING_DATA'].append(doi)

            author = create_training_data(entry['author'], text, 'AUTHOR')

            title_dict['TRAINING_DATA'].append(title)
            author_dict['TRAINING_DATA'].append(author)

            f.close()
    else:
        #para caso queira consertar os arquivos que faltarem na mão
        d.write(filename[0].strip() + '.txt' + ' ---->' + entry['title'] + '\n')
d.close()

print('artigos encontrados =', cont)

save_data("dados/TRAIN_DATA_PT/title_dict2.json", title_dict)
save_data("dados/TRAIN_DATA_PT/doi_dict2.json", doi_dict)
save_data("dados/TRAIN_DATA_PT/author_dict2.json", author_dict)