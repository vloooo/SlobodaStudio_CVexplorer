from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
import string
from nltk.corpus import stopwords
import pandas as pd
# import itertools
import numpy as np
# from gensim.models import FastText
# import gensim.downloader as api

stop_words = set(stopwords.words('english'))
np.set_printoptions(threshold=np.inf)


def print_most_sim(n, cof_simlr):
    df = pd.read_csv('data2.csv')
    cof_simlr = sorted(enumerate(cof_simlr), key=lambda x: x[1], reverse=True)
    strr = ''
    for i in range(n):
        response = df['responsibilities'].values[cof_simlr[i][0]].replace('{"', '').replace('"}', '') .replace('"', ' ')
        strr += response + '<b>    similar for ' + str(cof_simlr[i][1]) + '%</b><br>'
    return strr

def wrd_vec_match(req):
    df = pd.read_csv('data2.csv')

    # cleaning del punct and ' ' and digits and stop_words
    words = ''.join(df['responsibilities'].values).split('}{')
    translation = {ord(x): None for x in '{},'}
    second_trns = {ord(x): None for x in '"' + string.punctuation + string.digits}
    words = [i.translate(translation).lower() for i in words]
    words = [word_tokenize(i) for i in words]

    # create list consist of sentence-list, that contain words
    text = []
    for indx, i in enumerate(words):
        text.append([])
        for j in i:
            j = j.translate(second_trns)

            if "''" not in j and '``' not in j and '' is not j:
                text[indx].append(j)

    # reciving request
    request = set(req.translate(translation).translate(second_trns).lower().split(' '))

    # print(text)
    # word-vec models
    model1 = Word2Vec(text, min_count=1, size=200, workers=4, )
    model1.train(text, total_examples=len(text), epochs=300)

    # remove words that haven't word-base
    to_rm = []
    for i in request:
        try:
            model1[i]
        except KeyError:
            to_rm.append(i)
    request = [i for i in request if i not in to_rm]

    # merged = list(itertools.chain(*text))
    # for h in merged:
    #     print(model1.similarity('adaptive', h), h)
    # print(model1.most_similar('adaptive', topn=10))

    # calculate similarity for every candidates
    cof_simlrt = []
    for sent in text:
        sent_sim = []

        for i in request:
            try:
                sent_sim.append(np.max([model1.similarity(i, j) for j in sent]))
            except KeyError:
                continue
        mean = np.mean(sent_sim)

        if mean != 1:
            cof_simlrt.append(round(100 * mean, 2))
        else:
            cof_simlrt.append(round(100 * mean, 2))
        # cof_simlrt.append(round(np.mean(sent_sim), 2))


    return print_most_sim(10, cof_simlrt)

