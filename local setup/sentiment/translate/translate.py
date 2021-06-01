import pandas as pd
import os
from googletrans import Translator
import numpy as np

def trans(company, df):
	dir_path = os.path.abspath(os.path.dirname(__file__))
	output_path = os.path.join(dir_path, company + '_trans.CSV')
	
	if os.path.exists(output_path):
		df = pd.read_csv(output_path, encoding='utf-8').append(df)
		df.drop_duplicates(subset=['id'], inplace=True, keep='first')
		if 'english_text' in df.columns:
			df.rename(columns = {'english_text' : 'translated_text'}, inplace = True)
			print('eng')

	if 'translated_text' not in df.columns:
		df.insert(4, 'translated_text', None, True)

	for index, tweet in df.iterrows():
		if df.at[index, 'translated_text'] is None or df.at[index, 'translated_text'] is np.nan:
			print('got here?')
			swe_text = df.at[index, 'tweet_text']

			translator = Translator()
			en_text = translator.translate(swe_text, dest='en', src='sv').text
			print(en_text)

			df.at[index, 'translated_text'] = en_text
			if en_text == swe_text:
				print('probably blocked')
				df.drop(df.index[index:df.shape[0]-1], inplace=True)
				break
		
	
	df.to_csv(output_path, index = False, encoding='utf-8-sig') 
	return df

