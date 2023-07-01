from os import listdir
from os.path import isfile, join
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('bert-base-nli-mean-tokens')

fileNames = [f for f in listdir('./texto/') if isfile(join('./texto/', f))]
textos = []

for file in fileNames:
    print(file)

    # calcula a similaridade do arquivo com o texto original por cosine similarity

    f = open('./texto/' + file, 'r', encoding="utf-8")
    tmp = f.read()
    textos.append(tmp);

    f.close()

m = open('./dados/tmp.txt', 'r', encoding="utf-8")
input = m.read()

sentence_embeddings = model.encode(textos)
print(sentence_embeddings.shape)

#a partir dessa parte nÃ£o tÃ¡ funcionando
similaridade = cosine_similarity(
    [input],
    sentence_embeddings[0:]
)
