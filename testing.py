import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

df = pd.read_csv('../../outputs/processed_ws.csv', encoding='latin-1')
df.head()

df['processed_text'] = df['processed_text'].str.cat(df['hashtags'], sep =' ')
print(type(df['text'][0]))
import re
def preprocess(text):
#    print(type(text)
    text = re.sub(r'[^\w\d\s]', ' ', text)
    text = re.sub('[Ã]', ' ', text)
    return ' '.join(terms for terms in text.split())

df['processed_text'] = df.processed_text.apply(lambda row : preprocess(row))



#########################################################################################


import pandas as pd
import numpy as np
import seaborn as sns
import re 
import string
import matplotlib.pyplot as plt
import pandas_profiling as pp
import nltk
from nltk.stem import WordNetLemmatizer

df = pd.read_csv('../../outputs/final_dataset.csv', encoding='latin-1')

print(type(df))

df['hashtags'] = df['text'].apply(lambda x:re.findall('#\w*',x))
print(type(df['hashtags']))
df['hashtags']=df['hashtags'].astype(str).values.tolist()
print(df['hashtags'][0])
df['users'] = df['text'].apply(lambda x:re.findall('@\w*',x))
df['links'] = df['text'].apply(lambda x:re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',x, flags=re.MULTILINE))
df['links'] = df['links'].apply(lambda x:list(set(x)))

