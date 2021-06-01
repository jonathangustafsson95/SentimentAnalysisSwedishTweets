import nltk
import pandas as pd
import os, sys, getopt
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from googletrans import Translator
import emoji

cls = lambda: os.system('cls')
cls()

def main():

	if 'preprocessed_text' not in df.columns:
		df.insert(4, 'preprocessed_text', None, True)

	if 'polarity_scores' not in df.columns:
		df.insert(4, 'polarity_scores', None, True)
		
	if 'polarity_scores' not in df.columns:
		df.insert(4, 'polarity_scores', None, True)

	for index, tweet in df.iterrows():
		if df.at[index, 'preprocessed_text'] is None:
			print(index)
			text = df.at[index, 'translated_text']

			tokenizer = TweetTokenizer()
			tokenized_words = tokenizer.tokenize(text)

			lemmatizer = WordNetLemmatizer()
			lammatized_words = [lemmatizer.lemmatize(word.lower()) for word in tokenized_words]

			stopwords = nltk.corpus.stopwords.words("english")
			no_stopwords= [w for w in lammatized_words if w.lower() not in stopwords]

			alpha_words = [w for w in no_stopwords if remove_special_but_emojis(w)]

			sia = SentimentIntensityAnalyzer()
			preprocessed_text = ' '.join(alpha_words)
			df.at[index, 'preprocessed_text'] = preprocessed_text
			df.at[index, 'polarity_scores'] = sia.polarity_scores(preprocessed_text)


	df.to_csv(path, index = False, encoding='utf-8-sig') 


def remove_special_but_emojis(word):
	if word.isalpha():
		return True
	elif word in emoji.UNICODE_EMOJI['en']:
		return True
	else:
		return False


full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "c:"
long_options = ["csv="] 

try:
	if len(argument_list) < 2:
		raise Exception('You need to provide csv-file as arguments')

	arguments, values = getopt.getopt(argument_list, short_options, long_options)
	for current_argument, current_value in arguments:
		if current_argument in ("-c", "--csv"):
			csv = current_value

except getopt.error as err:
	# Output error, and return with an error code
	print(str(err))
	print(f'{full_cmd_arguments[0]} -c <inputfile>')
	sys.exit(2)
except Exception as e:
	print(str(e))
	sys.exit(2)

dir_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(dir_path, csv)

try:
	df = pd.read_csv(path, encoding='utf-8')
except Exception as e:
	print(str(e))
	sys.exit(2)

if __name__ == '__main__':
	main()

