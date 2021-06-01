import nltk
import pandas as pd
import numpy as np
import os
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import emoji
import stanza
from preprocess.lexikon.analysis import lex_analysis

def prep(company, df, en=False):
	if 'preprocessed_text' not in df.columns:
		df.insert(4, 'preprocessed_text', None, True)

	if en:
		return __en_prep(df, company)
	else:
		return __sv_prep(df, company)


def __sv_prep(df, company):

	dir_path = os.path.abspath(os.path.dirname(__file__))
	output_path = os.path.join(dir_path, company + '_prep_sv.CSV')
	if os.path.exists(output_path):
		df = pd.read_csv(output_path, encoding='utf-8')
		return df

	nlp = stanza.Pipeline(lang='sv')
	for index, tweet in df.iterrows():
		if df.at[index, 'preprocessed_text'] is None or df.at[index, 'preprocessed_text'] is np.nan:
			text = df.at[index, "tweet_text"].lower()
			text = text.replace(company, '')
			tokenizer = TweetTokenizer()
			tokenized_words = tokenizer.tokenize(text)

			stopwords = nltk.corpus.stopwords.words("swedish")
			no_stopwords= [w for w in tokenized_words if w.lower() not in stopwords]

			alpha_words = [w for w in no_stopwords if __remove_special_but_emojis(w)]
			if not alpha_words:
				df.drop([index])
			
			# Initiate document containing lemmatized words
			doc = nlp(' '.join(alpha_words))

			# Lemmatize words and join the words to a string
			lemmatized_words = [word.lemma for sentence in doc.sentences for word in sentence.words]
						
			df.at[index, 'preprocessed_text'] = ' '.join(lemmatized_words)

	df = lex_analysis(company, df)

	df.to_csv(output_path, index = False, encoding='utf-8-sig') 
	return df

def __en_prep(df, company):

	dir_path = os.path.abspath(os.path.dirname(__file__))
	output_path = os.path.join(dir_path, company + '_prep_en.CSV')
	if os.path.exists(output_path): 
		df = pd.read_csv(output_path, encoding='utf-8')
		return df

	for index, tweet in df.iterrows():
		text = df.at[index, "translated_text"]
		if type(text) is str and (text is not None or text is not np.nan):
			text = text.lower().replace(company, '')
			tokenizer = TweetTokenizer()
			tokenized_words = tokenizer.tokenize(text)

			stopwords = nltk.corpus.stopwords.words("english")
			no_stopwords= [w for w in tokenized_words if w.lower() not in stopwords]

			alpha_words = [w for w in no_stopwords if __remove_special_but_emojis(w)]
			if not alpha_words:
				df.drop([index])
			
			lemmatizer = WordNetLemmatizer()
			lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in alpha_words]
			
			df.at[index, 'preprocessed_text'] = ' '.join(lemmatized_words)

	df = lex_analysis(company, df, True)

	df.to_csv(output_path, index = False, encoding='utf-8-sig') 
	return df

def __remove_special_but_emojis(word):
	if word.isalpha():
		return True
	elif word in emoji.UNICODE_EMOJI['en']:
		return True
	else:
		return False


