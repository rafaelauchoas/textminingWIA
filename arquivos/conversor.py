from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from gensim.parsing.preprocessing import remove_stopwords
from os import listdir
from os.path import isfile, join
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import io
import re 
import os
# import codecs
import nltk

directory = os.getcwd().replace('\\', '/')
nltk.data.path.append(directory+'/nltk') 
nltk.download('punkt')
nltk.download('wordnet')
# nltk.download('averaged_perception_tagger')

# -----
fileNames = [f for f in listdir('./pdf/') if isfile(join('./pdf/', f))]
WNL = WordNetLemmatizer()

for file in fileNames:
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    name = file.split(".pdf")
    print(file)

    with open('./pdf/' + file, 'rb') as fh:

        for page in PDFPage.get_pages(fh,
                                    caching=True,
                                    check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    f = open('./texto/' + name[0] + '.txt', 'w', encoding="utf-8")
    e = open('./entidade/' + name[0] + '.txt', 'w', encoding="utf-8")
    # e = codecs.open('./entidade/' + name[0] + '.txt', "w", "utf-8")

    #pegar informações importantes
    e.write(text)

    #limpeza do texto
    text2 = re.sub(r'[^\w\s]', '', text)
    filtered_sentence = remove_stopwords(text2.lower())
    conj = word_tokenize(filtered_sentence) 

    for word in conj:
        f.write(WNL.lemmatize(word))
        f.write(' ')

    e.close()
    f.close()

m = open('./dados/input.txt', 'r', encoding="utf-8")
t = open('./dados/tmp.txt', 'w', encoding="utf-8")

textInput = m.read()
tmp0 = re.sub(r'[^\w\s]', '', textInput)
tmp1 = remove_stopwords(tmp0.lower())
tmp2 = word_tokenize(tmp1) 

for word in tmp2:
    t.write(WNL.lemmatize(word))
    t.write(' ')

t.close()
