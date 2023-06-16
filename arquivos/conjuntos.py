from os import listdir
from os.path import isfile, join

fileNames = [f for f in listdir('./pdf/') if isfile(join('./pdf/', f))]
# cria o template dos arquivos não avaliados
for file in fileNames:
    name = file.split(".pdf")
    print(file)
    
    f = open('./conjuntos/naoAvaliado/' + name[0] + '.txt', 'w', encoding="utf-8")
    f.write('"Título":\n')
    f.write('"Autores":\n')
    f.write('"Palavras-chave":\n')
    f.write('"Data de publicação":\n')
    f.write('"DOI ou identificador único":\n')
    f.close()

