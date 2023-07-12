from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from gensim.parsing.preprocessing import remove_stopwords
from os import listdir
from os.path import isfile, join
import json
import io
import re

fileNames = [f for f in listdir('./pdf/') if isfile(join('./pdf/', f))]

for file in fileNames:
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    tmp = file.split(".pdf")
    name = (tmp[0].replace(':','-')).split("-")
    print(name[1].strip())

    with open('./pdf/' + file, 'rb') as fh:

        for page in PDFPage.get_pages(fh,
                                    caching=True,
                                    check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    #corrigindo identificação errada de unicode do pdfminer
    tmp = text.replace('ﬁ', 'fi').replace ('ﬂ', 'fl').replace ('ﬀ', 'ff').replace ('ﬃ', 'ffi').replace ('ﬄ', 'ffl').replace ('ﬅ', 'ft')
    
    e = open('./entidade/' + name[1].strip() + '.txt', 'w', encoding="utf-8")

    #pegar informações importantes
    # json.dump(tmp2, e, ensure_ascii=False)
    e.write(tmp.replace(' \n', ' ').replace('\n', '').replace('\r', '').replace('  ', ' '))

    e.close()