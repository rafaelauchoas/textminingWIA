# from pdfminer.layout import LAParams, LTTextBox
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from gensim.parsing.preprocessing import remove_stopwords
from os import listdir
from os.path import isfile, join
import io
import re 

# -----
fileNames = [f for f in listdir('./pdf/') if isfile(join('./pdf/', f))]
# print(fileNames)

for file in fileNames:
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    # file = '1.PMC2110595.pdf'
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

    # print(text)
    f = open('./texto/' + name[0] + '.txt', 'w', encoding="utf-8")
    text2 = re.sub(r'[^\w\s]', '', text)
    # filtered_sentence = remove_stopwords(text2.lower()) //lowercase foi desconsiderado para não afetar a pesquisa de autor
    filtered_sentence = remove_stopwords(text2)
    f.write((filtered_sentence))

    # close open handles
    f.close()
