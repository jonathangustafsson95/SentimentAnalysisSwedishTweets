import pyodbc 
import os, sys, getopt
import pandas as pd

server = '' 
database = '' 
username = '' 
password = '' 

def main():
    cursor = conn.cursor() 
    for index, tweet in df.iterrows():
        print(df.at[index, 'tweet_polarity'])
        polarity = int(df.at[index, 'tweet_polarity'])
        cursor.execute("UPDATE stock.dbo.tweet SET tweet_polarity = ? WHERE tweet_id = ?", polarity, tweet.tweet_id)
        cursor.commit()
    cursor.close()


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
	conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
		'Server='+server+';'
		'Database='+database+';'
		'UID='+username+';'
		'PWD='+password+';'
		'Trusted_Connection=no;')

	main()
