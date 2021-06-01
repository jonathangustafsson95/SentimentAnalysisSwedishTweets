import pyodbc 
import pandas as pd
import tweepy
import getopt, sys
import os

server = '' 
database = '' 
username = '' 
password = '' 

TWITTER_API_KEY = ''
TWITTER_API_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "c:t:"
long_options = ["csv=", "table="]

try:
	if len(argument_list) < 4:
		raise Exception('You need to provide CSV file and table as arguments')

	arguments, values = getopt.getopt(argument_list, short_options, long_options)
	for current_argument, current_value in arguments:
		if current_argument in ("-c", "--csv"):
			csv = current_value
		elif current_argument in ("-t", "--table"):
			table = current_value

except getopt.error as err:
	# Output error, and return with an error code
	print(str(err))
	print(f'{full_cmd_arguments[0]} -c <inputfile> -d <table>')
	sys.exit(2)
except Exception as e:
	print(str(e))
	sys.exit(2)

dir_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(dir_path, csv)

try:
	df = pd.read_csv(path, header=None)
except Exception as e:
	print(str(e))
	sys.exit(2)

companies = df[0].values.tolist()

print(companies)

def main():
	for company in companies:
		'''Edit scince and until for day that data was lost.'''
		try:
			for tweet in tweepy.Cursor(api.search, q=company, since="2021-03-15", until="2021-10-20", result_type='recent', tweet_mode='extended', count=100, include_entities=False, lang="sv").items():	
				if hasattr(tweet, "retweeted_status"):  # Check if Retweet
					try:
						tweet_text = tweet.retweeted_status.extended_tweet["full_text"]
					except AttributeError:
						tweet_text = tweet.retweeted_status.full_text
				else:
					try:
						tweet_text = tweet.extended_tweet["full_text"]
					except AttributeError:
						tweet_text = tweet.full_text


				if company in str.lower(tweet_text):

					tweet_created_at = tweet.created_at
					tweet_id = tweet.id
					twitter_user_id = tweet.user.id
					twitter_user_followers_count = tweet.user.followers_count

					cursor = conn.cursor()
					cursor.execute(f'SELECT 1 FROM {table} WHERE tweet_id = ?', tweet.id) 
					exists = cursor.fetchone()
					if exists:
						print(f'Tweet {tweet.id} already exist in DB')
					else:
						cursor.execute(f"INSERT INTO {table} (company, tweet_created_at, tweet_id, tweet_text, twitter_user_id, twitter_user_followers_count) VALUES(?,?,?,?,?,?)", company, tweet_created_at, tweet_id, tweet_text, twitter_user_id, twitter_user_followers_count)
						conn.commit()
						print(f'One tweet: \n{tweet.full_text} \n created at: \n{tweet.created_at} \n was inserted in DB\n')

					cursor.close()
		except Exception as e:
			print('Something happend')
			print(e)


if __name__ == '__main__':
	conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
		'Server='+server+';'
		'Database='+database+';'
		'UID='+username+';'
		'PWD='+password+';'
		'Trusted_Connection=no;')

	auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth, 
		wait_on_rate_limit=True,
		wait_on_rate_limit_notify = True,
		retry_count = 10, #retry 10 times
		retry_delay = 30) #seconds to wait for retry
	main()
