import pandas as pd
import numpy as np
import os
from nltk.sentiment import SentimentIntensityAnalyzer as SentimentIntensityAnalyzer_en
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SentimentIntensityAnalyzer_sv

def lex_analysis(company, df, en=False):

	if 'polarity_scores' not in df.columns:
		df.insert(4, 'polarity_scores', None, True)

	dir_path = os.path.abspath(os.path.dirname(__file__))	
	if en:
		output_path = os.path.join(dir_path, company + '_lex_en.CSV')
		sia = SentimentIntensityAnalyzer_en()
	else:
		output_path = os.path.join(dir_path, company + '_lex_sv.CSV')
		sia = SentimentIntensityAnalyzer_sv()
	
	for index, tweet in df.iterrows():
		text = df.at[index, 'preprocessed_text']
		if type(text) is str and (text is not None or text is not np.nan):
			df.at[index, 'polarity_scores'] = sia.polarity_scores(text)
	
	df.to_csv(output_path, index = False, encoding='utf-8-sig') 
	return df