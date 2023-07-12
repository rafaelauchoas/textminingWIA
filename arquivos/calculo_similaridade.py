###########################################################################################################
## BASEADO NO CÓDIGO https://www.kaggle.com/code/adepvenugopal/nlp-text-similarity-using-glove-embedding ##
###########################################################################################################

import numpy as np
from os import listdir
from os.path import isfile, join
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import pandas as pd
import scipy
import seaborn as sns
import matplotlib.pyplot as plt

# model = SentenceTransformer('bert-base-nli-mean-tokens')

m = open('./dados/tmp.txt', 'r', encoding="utf-8")
entrada = m.read()
m.close()

fileNames = [f for f in listdir('./texto/') if isfile(join('./texto/', f))]
textos = []

def loadGloveModel(gloveFile):
    print ("Loading Glove Model")
    with open(gloveFile, encoding="utf8" ) as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print ("Done.",len(model)," words loaded!")
    return model

def preprocess(raw_text):
    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split 
    words = letters_only_text.lower().split()

    # remove stopwords
    stopword_set = set(stopwords.words("portuguese"))
    cleaned_words = list(set([w for w in words if w not in stopword_set]))

    return cleaned_words

def cosine_distance_between_two_words(word1, word2):
    return (1- scipy.spatial.distance.cosine(model[word1], model[word2]))

def calculate_heat_matrix_for_two_sentences(s1,s2):
    s1 = preprocess(s1)
    s2 = preprocess(s2)
    result_list = [[cosine_distance_between_two_words(word1, word2) for word2 in s2] for word1 in s1]
    result_df = pd.DataFrame(result_list)
    result_df.columns = s2
    result_df.index = s1
    return result_df

def cosine_distance_wordembedding_method(s1, s2):
    vector_1 = np.mean([model[word] for word in preprocess(s1)],axis=0)
    vector_2 = np.mean([model[word] for word in preprocess(s2)],axis=0)
    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    o.write("Similaridade: ",round((1-cosine)*100,2),'%','\n')
    print('Word Embedding method with a cosine distance asses that our two sentences are similar to',round((1-cosine)*100,2))

def heat_map_matrix_between_two_sentences(s1,s2):
    df = calculate_heat_matrix_for_two_sentences(s1,s2)
    fig, ax = plt.subplots(figsize=(5,5)) 
    ax_blue = sns.heatmap(df, cmap="YlGnBu")
    # ax_red = sns.heatmap(df)
    print(cosine_distance_wordembedding_method(s1, s2))
    return ax_blue

model = loadGloveModel('./dados/glove.6B.50d.txt')
o = open('./dados/output.txt', 'w', encoding="utf-8")

for file in fileNames:
    f = open('./texto/' + file, 'r', encoding="utf-8")
    tmp = f.read()
    heat_map_matrix_between_two_sentences(entrada,tmp)
    f.close()

o.close()