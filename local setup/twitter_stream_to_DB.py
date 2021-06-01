#!/home/challe/twitterstream/venv/bin/python

import pandas as pd
import pyodbc
import time
import tweepy
import logging

class StreamListener(tweepy.StreamListener):
	def set_conn(self, conn):
		self.conn = conn

	def on_status(self, status):
		if hasattr(status, "retweeted_status"):  # Check if Retweet
			try:
				tweet_text = status.retweeted_status.extended_tweet["full_text"]
			except AttributeError:
				tweet_text = status.retweeted_status.text
		else:
			try:
				tweet_text = status.extended_tweet["full_text"]
			except AttributeError:
				tweet_text = status.text

		match, company = find_substring(str.lower(tweet_text))
		if match:
			tweet_created_at = status.created_at
			tweet_id = status.id
			twitter_user_id = status.user.id
			twitter_user_followers_count = status.user.followers_count

			db_handler.store_data(company, tweet_created_at, tweet_id, tweet_text, twitter_user_id, twitter_user_followers_count)

	def on_error(self, status_code):
		logger.error(status_code)
		return False

class DatabaseHandler():
	def __init__(self):
		self.conn = self.db_connect()

	def store_data(self, company, tweet_created_at, tweet_id, tweet_text, twitter_user_id, twitter_user_followers_count):
		stored = False
		while not stored:
			try:
				cursor = self.conn.cursor()
				cursor.execute("INSERT INTO stock.dbo.tweet (company, tweet_created_at, tweet_id, tweet_text, twitter_user_id, twitter_user_followers_count) VALUES(?,?,?,?,?,?)", company, tweet_created_at, tweet_id, tweet_text, twitter_user_id, twitter_user_followers_count)
				self.conn.commit()
				cursor.close()
				stored = True
			except pyodbc.Error as e:
				logger.error(e)
				self.conn = self.db_connect()
			except Exception as e:
				logger.error(e)

	def db_connect(self):
		while True:
			try:
				conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
			              'Server='+server+';'
			              'Database='+database+';'
			              'UID='+username+';'
			              'PWD='+password+';'
			              'Trusted_Connection=no;')
			except Exception as e:
				logger.error(e)
			else:
				logger.info('connected to database')
				return conn

def find_substring(text):
	for company in companies:
		if company in text:
			return True, company
	return False, None

def main():
	while True:
		try:
			streamListener = StreamListener()
			stream = tweepy.Stream(auth = api.auth, listener=streamListener, tweet_mode="extended")
			stream.filter(track=companies, languages=['sv'])
		except Exception as e:
			logger.error(e)


server = '' 
database = '' 
username = '' 
password = '' 

TWITTER_API_KEY = ''
TWITTER_API_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

handler = logging.FileHandler('log.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', style='%'))
logger.addHandler(handler)

df = pd.read_csv(r"companies.csv", header=None)
companies = df[0].values.tolist()

if __name__ == "__main__":
	auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	db_handler = DatabaseHandler()

	main()

