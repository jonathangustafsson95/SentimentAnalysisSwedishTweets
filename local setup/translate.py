import pandas as pd
import os, sys, getopt
from googletrans import Translator
import numpy as np

cls = lambda: os.system('cls')
cls()

def main(df):
	if 'translated_text' not in df.columns:
		df.insert(4, 'translated_text', None, True)

	if csv.split('.')[0][5:] == '_trans':
		output_path = input_path
	else:
		output_path = os.path.join(dir_path, csv.split('.')[0] + '_trans.CSV')

	if os.path.exists(output_path):
		df = pd.read_csv(output_path, encoding='utf-8').append(df)
		df.drop_duplicates(subset=['id'], inplace=True, keep='first')

	for index, tweet in df.iterrows():
		if df.at[index, 'translated_text'] is None or df.at[index, 'translated_text'] is np.nan:
			swe_text = df.at[index, 'tweet_text']

			translator = Translator()
			en_text = translator.translate(swe_text, dest='en', src='sv').text

			df.at[index, 'translated_text'] = en_text
			if en_text == swe_text:
				print('probably blocked')
				break
	
	df.to_csv(output_path, index = False, encoding='utf-8-sig') 


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
input_path = os.path.join(dir_path, csv)
print(input_path)

try:
	df = pd.read_csv(input_path, encoding='utf-8')
except Exception as e:
	print(str(e))
	sys.exit(2)

if __name__ == '__main__':
	main(df)

