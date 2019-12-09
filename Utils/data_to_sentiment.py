"""
    Run from inside C9 in AWS EC2 instance
"""

import csv
import json
import boto3

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
upper_lim = 2000

with open('data_cleaned.csv', encoding = "utf8", errors = "ignore") as csv_file_read:
    with open('sentiments.csv', "a+", encoding = "utf8", errors = "ignore") as csv_file_write:
        csv_writer = csv.writer(csv_file_write, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_reader = csv.reader(csv_file_read, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count >= upper_lim:
                break
            #first row is headers, we set up headers for result file as well
            if line_count == 0:
                csv_writer.writerow(row + ['Sentiment', 'Mixed', 'Negative', 'Neutral', 'Positive'])
                line_count += 1
                continue

            #send request to sentiment analysis with text (row[6])
            temp = json.dumps(comprehend.detect_sentiment(Text=row[6], LanguageCode='en'), sort_keys=True, indent=4)

            #convert to a dictionary for easier accessing
            json_dict = json.loads(temp)
            sentiment = json_dict["Sentiment"]
            scores = json_dict["SentimentScore"]

            #append the data to the results file
            data_to_add = [sentiment, scores["Mixed"],scores["Negative"],scores["Neutral"],scores["Positive"]]
            csv_writer.writerow(row + data_to_add)
            print(line_count, data_to_add)
            line_count +=1

        print("processed lines:", line_count)

#can combine to read input, parse into the text, send text to aws, write response back.
