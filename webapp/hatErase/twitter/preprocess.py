from sklearn.base import TransformerMixin, BaseEstimator
import re
import nltk 
from nltk import WordNetLemmatizer
import multiprocessing as mp


class TextPreprocessor(BaseEstimator, TransformerMixin):

  def __init__(self, variety = 'BrE', user_abbrevs={}, n_jobs=1):
    self.variety = variety
    self.user_abbrevs = user_abbrevs
    self.n_jobs = n_jobs
  
  def fit(self, X, y = None):
    return self
  
  def transform(self, X, *_):
    # incomplete will be completed later
    # X_copy = X.copy()
    X_copy = X
    partitions = 1
    cores = mp.cpu_count()

    if self.n_jobs <= -1:
      partition = cores
    elif self.n_jobs <= 0:
      return X_copy.apply(slef._preprocess_text)
    else:
      partitions = min(self.n_jobs, cores)
    
    data_split = np.array_split(X_copy,partitions)
    pool = mp.Pool(cores)
    data = pd.concat(pool.map(self._preprocess_part, data_split))
    pool.close()
    pool.join()

    return data
  
  def _preprocess_part(self, part):
    return part.apply(self._preprocess_text)
  
  def _preprocess_text(self, text):
    hashtags = re.findall('#\w*',text)
    users = re.findall('@\w*',text)
    links = re.findall('(https|http)?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text, flags=re.MULTILINE)
    links = list(set(links))
    # Removing Links
    text =  re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', ' ', text, flags=re.MULTILINE)
    # Removing mentions and hashtags
    text = re.sub(r"#(\w+)", ' ', text, flags=re.MULTILINE)
    text = re.sub(r"@(\w+)", ' ', text, flags=re.MULTILINE)
    # Removing punctuations
    text = re.sub(r'[^\w\d\s]', ' ', text)
    # convert to lower case
    text = re.sub(r'^\s+|\s+?$', ' ', text.lower())
    # Removing digits
    text = re.sub(r'\d', ' ', text)
    # Removing other symbols
    text = re.sub('[ãâªð³ÂÃÃ±¤¡¥¶¦§_®¯¹¾²µ½¼º]+', ' ', text)
    # collapse all white spaces
    text = re.sub(r'\s+', ' ', text)
    # text = re.sub('[Ã]', ' ', str(text))
    # remove stop words and perform stemming
    stop_words = nltk.corpus.stopwords.words('english')
    # 
    lemmatizer = WordNetLemmatizer()
    text = ' '.join(lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words)

    return [hashtags, users, links, [text]]

  

  def predict(self, text):
    tfidf_text = tfidf_vec.fit_transform(text)

    return model.predict(tfidf_text)[:,1]

