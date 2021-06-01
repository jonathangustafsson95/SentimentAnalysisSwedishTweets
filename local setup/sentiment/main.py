import os, sys, getopt
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from translate.translate import trans
from preprocess.preprocess import prep
from ml.analysis import ml

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


def main(df):
    company = csv.split('.')[0]
    #df_sv = df.copy()
    #df_en = df

    #df_en = trans(company, df_en)
    #df_en = prep(company, df_en, True)

    #df_sv = prep(company, df_sv)
    
    ml(company, df)


if __name__ == '__main__':
    main(df)
