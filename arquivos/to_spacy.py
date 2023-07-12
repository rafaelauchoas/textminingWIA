import json
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

#ARQUIVO PARA CRIAÇÃO DE ARQUIVOS .SPACY (roda separado para traver menos)
f = open('./dados/TRAIN_DATA_PT/title_test.json', 'r', encoding="utf-8")
train_en = f.read()
f.close

nlp = spacy.blank("pt") # load a new spacy model
db = DocBin() # create a DocBin object

lista_en = json.loads(train_en)

for text, annot in tqdm(lista_en["TRAINING_DATA"]): # data in previous format
    doc = nlp.make_doc(text) # create doc object from text
    ents = []
    for start, end, label in annot["entities"]: # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    try:
        doc.ents = ents # label the text with the ents
        db.add(doc)
    except:
        print(text, annot)
db.to_disk("./dados/TRAIN_DATA_PT/test_title_pt.spacy") # save the docbin object
