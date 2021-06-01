import pyodbc 
import os, sys, getopt
import time

cls = lambda: os.system('cls')
cls()

server = '' 
database = '' 
username = '' 
password = '' 


def main():
	accepted_ints = [-1, 0, 1, 9]

	while True:
		print('Enter company name (blank to exit):')
		company = input()
		cursor = conn.cursor() 
		if nine is None:
			cursor.execute("SELECT * FROM stock.dbo.tweet WHERE company = ? AND tweet_polarity IS NULL", company)
		else:
			cursor.execute("SELECT * FROM stock.dbo.tweet WHERE company = ? AND (tweet_polarity IS NULL OR tweet_polarity = ?)", company, 9)
		tweets = cursor.fetchall()
		for tweet in tweets:
			cls()
			print(tweet.tweet_text)
			while True:
				print('\nInput polarity (neg=-1, neu=0, pos=1 & ?=9):')
				polarity = int(input())

				if polarity in accepted_ints:
					cursor.execute("UPDATE stock.dbo.tweet SET tweet_polarity = ? WHERE tweet_id = ?", polarity, tweet.tweet_id)
					cursor.commit()
					print(f'Polarity {polarity} inserted for tweet.')
					time.sleep(1.5)
					break
				else:
					print('You can only use ints, -1, 0, 1 and 9')

		if company == "":
			break
		else:
			print(f'No tweets for {company} or you are DONE')
		cursor.close()


full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "n"
long_options = ["nine"] 

try:
	nine = None
	arguments, values = getopt.getopt(argument_list, short_options, long_options)
	for current_argument, current_value in arguments:
		if current_argument in ("-n", "--nine"):
			nine = current_value

except getopt.error as err:
	# Output error, and return with an error code
	print(str(err))
	print(f'{full_cmd_arguments[0]} -c <inputfile>')
	sys.exit(2)
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
