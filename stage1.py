from twython import Twython
import json
import csv

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# Create our query
# query = {'q': 'learn',
#         'result_type': 'popular',
#         'count': 10,
#         'lang': 'en',
#         }
# import pandas as pd
# # Search tweets
# dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
# for status in python_tweets.search(**query)['statuses']:
# 	dict_['user'].append(status['user']['screen_name'])
# 	dict_['date'].append(status['created_at'])
# 	dict_['text'].append(status['text'])
# 	dict_['favorite_count'].append(status['favorite_count'])

# Structure data in a pandas DataFrame for easier manipulation
# df = pd.DataFrame(dict_)
# df.sort_values(by='favorite_count', inplace=True, ascending=False)
# print(df.head(5))

categories = []
with open('input.csv', encoding = "utf8", errors = "ignore") as csv_file_read:
	queries = []
	csv_reader = csv.reader(csv_file_read, delimiter=',')
	next(csv_reader)

	for line in csv_reader:
		username = line[0]
		category = line[1]
		if category not in categories:
			categories.append(category)
		queries.append(({'screen_name': username}, category))

	outputs = []
	for query in queries:
		for result in python_tweets.get_user_timeline(**(query[0])):
			tweet = result['text']
			tweetid = result['id']
			outputs.append([query[0]['screen_name'], tweetid, tweet, query[1]])

	# this would overwrite the previous file, be careful
	with open('output.csv', "w", encoding = "utf8", errors = "ignore") as csv_file_write:
		csv_writer = csv.writer(csv_file_write, delimiter=',', quoting=csv.QUOTE_MINIMAL)

		# csv_writer.writerow(['Handle', 'TweetID', 'Tweet', 'Category'])
		# for output in outputs:
		# 	csv_writer.writerow(output)

		csv_writer.writerow(['Handle', 'TweetID', 'Tweet'] + categories)
		for output in outputs:
			csv_writer.writerow(output[:3] + [ 1 if output[3] == category else 0 for category in categories])

