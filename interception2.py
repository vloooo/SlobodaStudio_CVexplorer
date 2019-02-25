import pandas as pd
import string
from nltk.corpus import stopwords




def intrsp(req):
    translation = {ord(x): None for x in '{}'}
    second_trns = {ord(x): None for x in '"' + string.digits}
    df = pd.read_csv('data2.csv')
    stop_words = set(stopwords.words('english'))

    # create expiriance list
    exp = req.translate(translation).translate(second_trns).lower().split(',')

    intrspt = []
    for i, index in zip(df['responsibilities'].values, df['responsibilities'].index):
        i = i.replace('{"', ' ').replace('"}', ' ').translate(second_trns).lower().split(',')
        for j in exp:
            for k in i:
                if j in k and i not in intrspt:
                    intrspt.append(i)

    str = ''
    for i in intrspt:
        i = ','.join(i)
        str += i + ' <br> '
    return str

# intrsp('Adaptive actuating')