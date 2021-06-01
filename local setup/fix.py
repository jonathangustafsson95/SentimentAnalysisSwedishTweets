import os, sys, getopt
import pandas as pd


def main(df):
    if 'english_text' in df.columns:
        df.rename(columns = {'english_text' : 'translated_text'}, inplace = True)
        print('Renamed english_text column')

    if 'Unnamed: 0' in df.columns:
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
        print('Dropped Unnamed: 0 column')

    if 'tweet_type' in df.columns:
        df.drop(['tweet_type'], axis=1, inplace=True)
        print('Dropped tweet_type column')


    print('input company:')
    company = input()
    dir_path = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(dir_path, company + '.CSV')

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

try:
    df = pd.read_csv(input_path, encoding='utf-8')
except Exception as e:
    print(str(e))
    sys.exit(2)

if __name__ == '__main__':
	main(df)

