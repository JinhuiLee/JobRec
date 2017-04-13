import pymongo
import pprint
import nltk
import logging
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from gensim import corpora, models, similarities
import json

class RecIntern():
	def __init__(self):
		logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
		client = MongoClient('localhost', 27017)
		db = client.indeed
		jobs = db.intern
		docs = jobs.find()
		descs = []
		self.titles = []
		self.urls = []
		self.company = []
		for doc in docs:
			descs = descs + [doc['desp']]
			self.titles = self.titles + [doc['title']]
			self.urls = self.urls + [doc['detailUrl']]
			self.company = self.company + [doc['company']]
		print(len(descs))
		texts_tokenized = [[word.lower() for word in word_tokenize(document)] for document in descs]
		print('Tokenizing ... ...'+ str(len(texts_tokenized)))
		english_stopwords = stopwords.words('english')
		texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]
		print('Filtering stopwords ... ...' + str(len(texts_filtered_stopwords)))
		english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
		texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
		print('Filtering punctuations ... ...' + str(len(texts_filtered)))
		self.keywords = dict()
		with open("techDict.txt") as f:
			content = f.readlines()
		for c in content:
			self.keywords[c.lower().strip()] = 1
		# print keywords
		texts = [[word for word in docment if word in self.keywords] for docment in texts_filtered]
		print('stemming ... ...' + str(len(texts)))
		# print(texts)
		self.dictionary = corpora.Dictionary(texts)
		print self.dictionary.values()
		if not self.dictionary:
			print('not good ... ...')
		corpus = [self.dictionary.doc2bow(text) for text in texts]
		tfidf = models.TfidfModel(corpus)
		corpus_tfidf = tfidf[corpus]
		self.lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=100)
		self.index = similarities.MatrixSimilarity(self.lsi[corpus])
	
	def txt2feature(self,doc):
		english_stopwords = stopwords.words('english')
		english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
		f = [word.lower() for word in word_tokenize(doc)]
		f = [word for word in f if not word in english_stopwords]
		f = [word for word in f if not word in english_punctuations]
		f = [word for word in f if word in self.keywords]
		return f


	def recommend(self,data):
		# with open("test_data.txt") as f:
		# 	test = f.read().decode('utf-8')
		ml_course = self.txt2feature(data)
		print(ml_course)
		ml_bow = self.dictionary.doc2bow(ml_course)
		ml_lsi = self.lsi[ml_bow]
		print "here"
		print ml_lsi
		sims = self.index[ml_lsi]
		sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
		res = []
		i = 0
		for item in sort_sims[0:min(50,len(sort_sims))]:
			index = item[0]
			res = res + [ {"index": i ,"url":self.urls[index], "title" : self.titles[index], "company" : self.company[index]} ]
			i = i + 1 
		return res