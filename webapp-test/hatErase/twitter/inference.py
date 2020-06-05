import re
import nltk 
from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib 

# importing ML model
import pickle
model_path = "twitter/models/LR_model.sav"
model = pickle.load(open(model_path, 'rb'))

# importng the saved tfidf vector
vocab_path = "twitter/models/vocabulary.pickle"
tfidf_vocab = pickle.load(open(vocab_path, 'rb'))
tfidf_vec = TfidfVectorizer(analyzer='word', ngram_range=(1,3), max_features=10000, vocabulary = tfidf_vocab)
# we can only use the vocab of the saved tfidf vector not it as completely
class Inference():

	def __init__(self):
		self.model = model
		self.tfidf_vec = tfidf_vec

	def fit_transform(self,text):
		# print(tex)
		tfidf_text = tfidf_vec.fit_transform([text])
		return tfidf_text
		

	def preprocess_text(self, text):
		
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

		return hashtags, users, links, text



	def predict(self, tfidf_text):
		pred = self.model.predict(tfidf_text)[0]
		# print(pred)
		return pred

