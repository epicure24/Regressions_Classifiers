import requests
import base64
import json
import re
import pandas as pd
from requests_oauthlib import OAuth1
import Twitter_key
from nltk import ngrams
from collections import Counter
import pandas as pd
from gensim.summarization import keywords
from name_entity import name_entity_analysis
from yt_sugg_que import main_function
from urllib.request import urlopen
from urllib.parse import parse_qs
import urllib
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


bearer_token =xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
search_headers = {
    'Authorization': 'Bearer {}'.format(bearer_token)    
}

#FUNCTION TO EXTRACT THE LATEST TWEET ID FROM ANY USER ACCOUNT USING HIS 'SCREENNAME' OR 'USERNAME'
def get_latest_tweet(screen_name):
	url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count=1".format(screen_name)
	resp = requests.get(url, headers=search_headers)
	tweet_id = json.loads(resp.text)[0]['id']
	return tweet_id

#FUNCTION TO GET THE TOTAL NUMBER OF FAVORITE COUNT AND RETWEET COUNT ON ANY TWEET USING TWEET_ID
def get_tweet_stat(tweet_id):
	stat={}
	url = "https://api.twitter.com/1.1/statuses/show.json?id={}".format(tweet_id)
	resp = requests.get(url, headers=search_headers)
	stat['favorite'] = json.loads(resp.text)['favorite_count']
	stat['retweet'] = json.loads(resp.text)['retweet_count']
	return stat


#FUNCTION TO GET REPLIES ON ANY TWEET GIVEN THE TWEET ID, ACCESS TOKEN AND ACCESS TOKEN SECRET OF THE USER ACCOUNT
def get_replies(tweet_id, access_token, access_token_secret):
	twitter = OAuth1(client_key=XXXXXXXXXXXXXXXXXXXXXXXXX 
                        client_secret=XXXXXXXXXXXXXXXXXXXXXXX
                        resource_owner_key= access_token,
                        resource_owner_secret= access_token_secret
                        )
	max_pages=10
	comments = []
	url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?since_id{}=&count=100'.format(tweet_id)
	list_id =[]
	count = 0
	for i in range(0, max_pages):
	
		resp = requests.get(url, auth=twitter)
		
		url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?since_id={}&count=100'.format(tweet_id)

		out= json.loads(resp.text)
		#print(out)
		for i in out:
			count +=1
			list_id.append(i['id'])
			if i['in_reply_to_status_id']==tweet_id:
			    comments.append(i.get('text'))
		url = url + "&max_id={}".format(min(list_id)-1)
	
	#cleaning the comments by removing urls,mentions and new_lines
	cleaned_comments = []
	for text in comments:
		text = re.sub(r'@[\w]+','',text)
		text = re.sub(r'https://t.co/[\w]+','',text)
		text = re.sub(r'\n','',text)
		cleaned_comments.append(text)
	
	#hashtags
	word_list = []
	for i in comments:
		word_list.append(i.split())

	hashtags = []
	for i in word_list:
		for j in i:
			if j.startswith("#"):
				hashtags.append(j)

	
	return cleaned_comments, hashtags	

#FUNCTION TO DO SENTIMENT ANALYSIS OF REPLIES LIST PASSED TO IT
def sentiment_analysis(comments_list):
	sentiment=[]
	neg = 0
	pos = 0
	neu = 0
	comments_list = list(set(comments_list))
	for i in comments_list:
		vs = analyzer.polarity_scores(i)
	 
		neg += vs['neg']
		pos += vs['pos']
		neu += vs['neu']

	neg_em = neg
	pos_em = pos
	neu_em = neu
	sentiment = [{ "x":'negative', 'y':neg_em },{'x':'positive','y':pos_em},{'x':'neutral', 'y':neu_em}]
	return sentiment

#FUNCTION TO SPLIT THE SENTENCE INTO WORDS
def generate_keywords(cleaned_comments):
	keyword_list=[]
	keyword_list.append(keywords(''.join(cleaned_comments), scores = True, lemmatize = True))
	keyword_list_final = [x[0] for x in sum(keyword_list,[])]
	return keyword_list_final

#FUNCTION TO DO VARIOUS ANALYSIS
def tweet_analysis(screen_name, access_token, token_secret):
	result = {}
	tweet_id = get_latest_tweet(screen_name)
	stat = get_tweet_stat(tweet_id)
	cleaned_comments, hashtags = get_replies(tweet_id, access_token, token_secret)
	
	#LIST OF TWEET REPLIES IS PASSED THROUGH 'main function' called from the yt_sug_que file 
	#this function separates the list into suggestions and questions if present
	suggestions, questions = main_function(cleaned_comments,'twitter')

	
	words_freq = Counter(generate_keywords(cleaned_comments))
	result['keywords'] = [{'text': word, 'value':int(count)} for word, count in words_freq.items()]
	result['sentiment_analysis'] = sentiment_analysis(cleaned_comments)
	result['suggestions'] = suggestions
	result['questions'] = questions
	result['hashtags'] = hashtags
	
	#name_entity is a function that extracts the ENTITY or nouns from the comments
	result['aspect_analysis'] = name_entity_analysis(cleaned_comments) 
	result['stats']=[{'heading':"likes", 'count': stat['favorite'] },
{'heading':"retweets", 'count': stat['retweet']}]

	print(result)
	return result



#FUNCTION TO POST TWEETS ON THE USER TIMELINE
def post_tweet(text, access_token, access_token_secret):
	twitter = OAuth1(client_key=Twitter_key.consumer_key, 
                        client_secret=Twitter_key.consumer_secret,
                        resource_owner_key= access_token,
                        resource_owner_secret= access_token_secret
                        )

	status = urllib.parse.quote_plus(text)
	url ='https://api.twitter.com/1.1/statuses/update.json?status={}'.format(status)
	resp = requests.post(url, auth=twitter)
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

#GET THE TRENDING HASHTAGS TRENDING RIGHT NOW
def get_trending_hashtags():
	#23424848 is the WOEID (where on eath id) of INDIA
	url = "https://api.twitter.com/1.1/trends/place.json?id={}&count=100".format(23424848)
	resp = requests.get(url, headers=search_headers)
	trends = json.loads(resp.text)
	trends_list =[]
	for trend in trends[0]['trends']:
		keys = trend['name']
		if keys.startswith("#"):
			trends_list.append(trend['name'])
	
	return trends_list



