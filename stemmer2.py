import pandas as pd
# from nltk.stem.wordnet import WordNetLemmatizer
# import nltk
import string
from nltk.stem import PorterStemmer
# from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import numpy as np
stop_words = set(stopwords.words('english'))
np.set_printoptions(threshold=np.inf)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

percent_to_match = 0.5

def create_bag(words):
    word_vec = set(words)
    word_vec.remove('')
    word_vec = {k: v for v, k in enumerate(word_vec)}
    return word_vec

def print_most_sim(n, cof_simlr):
    df = pd.read_csv('data2.csv')
    cof_simlr = sorted(enumerate(cof_simlr), key=lambda x: x[1], reverse=True)
    strr = ''
    for i in range(n):
        response = df['responsibilities'].values[cof_simlr[i][0]].replace('{"', '').replace('"}', '').replace('"', ' ')
        strr += response + '<b>    similar for ' + str(cof_simlr[i][1]) + '%</b><br>'
    return strr

def stemm_match(req):
    # loading exel and rename some columns
    df = pd.read_csv('data2.csv')

    # read data
    words = ''.join(df['responsibilities'].values)

    # cleaning del punct and ' ' and digits and stop_words
    translation = {ord(x): None for x in '{},'}
    second_trns = {ord(x): None for x in '"' + string.punctuation + string.digits}
    words = words.translate(translation).lower().split('""')
    words = ' '.join(words).translate(second_trns).split(' ')
    words = [x for x in words if x not in stop_words]

    # stemming
    porter = PorterStemmer()
    # englishStemmer = SnowballStemmer("english")
    lema_word = [porter.stem(token) for token in words]

    # create bag of words
    encoder = create_bag(lema_word)

    # clean and encode all instances of responsobilities
    candidates_vecs = np.zeros((len(df['responsibilities'].values), len(encoder)))

    for i, index in zip(df['responsibilities'].values, df['responsibilities'].index):
        i = set(i.replace('","', ' ').replace('{"', ' ').replace('"}', ' ').translate(second_trns).lower().split(' '))
        i.remove('')
        i = [porter.stem(token) for token in i if token not in stop_words]
        for j in i:
            candidates_vecs[index, encoder[j]] = 1

    # clean and encode request
    request = set(req.translate(translation).translate(second_trns).lower().split(' '))
    try:
        request.remove('')
    except KeyError:
        pass
    request = [porter.stem(token) for token in request if token not in stop_words]
    req_vec = np.zeros(len(encoder))

    for i in request:
        try:
            req_vec[encoder[i]] = 1
        except KeyError:
            encoder[i] = len(encoder)

    # multiply all vectors and find count of interseptions
    crl = np.multiply(candidates_vecs, req_vec)
    counter = 0
    # print('Request Lema', request)
    # print('Responses: \n')
    # strr = ''
    cof_simlrt = []
    for indx, row in zip(range(len(crl)), crl):
        similarity = row.sum()
        cof_simlrt.append(round(100 * similarity / len(request), 2))
        # if similarity / len(request) >= percent_to_match:
        #     response = df.loc[indx, 'responsibilities'].replace('{"', '').replace('"}', '')
            # strr += response + '<b>    similar for ' + str(round(similarity / len(request), 2)) + '%</b><br>'
            # print(request)
            # print('\nmatched by:')
            # for k in request:
            #     if k in response:
            #         print(k)
            # print('\n')
    return print_most_sim(10, cof_simlrt)
    # print(counter)