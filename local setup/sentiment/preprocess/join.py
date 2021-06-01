import pandas as pd
import os, sys, getopt
import glob

def main():

	dir_path = os.path.abspath(os.path.dirname(__file__))
	output_path = os.path.join(dir_path, lang + '.CSV')
	
	df = pd.DataFrame()
	col_list = ["company", "polarity_scores", "preprocessed_text", "tweet_polarity"]

	for filename in glob.glob(os.path.join(dir_path, '*_' + lang + '.CSV')):
		path = os.path.join(dir_path, filename)
		df = pd.concat([df, pd.read_csv(path, encoding='utf-8', usecols=col_list)])
	
	df = df[~(df['tweet_polarity'] > 1)]

	df.to_csv(output_path, index = False, encoding='utf-8-sig') 

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "l:"
long_options = ["lang="] 
allowed_langs = ['sv', 'en']

try:
	if len(argument_list) < 2:
		raise Exception('You need to provide language as arguments')

	arguments, values = getopt.getopt(argument_list, short_options, long_options)
	for current_argument, current_value in arguments:
		if current_argument in ("-l", "--lang"):
			lang = current_value
			if lang not in allowed_langs:
				raise Exception('Language has to be "sv" or "en"')


except getopt.error as err:
	# Output error, and return with an error code
	print(str(err))
	print(f'{full_cmd_arguments[0]} -l <sv/ev>')
	sys.exit(2)
except Exception as e:
	print(str(e))
	sys.exit(2)


if __name__ == '__main__':
	main()