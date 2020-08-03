from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import Twitter_key
from nltk import word_tokenize, pos_tag, ngrams
import pandas as pd 
import numpy as np 
from comment_extraction import CommentExtractor
from time import time
import collections
import ast
from gensim.summarization import keywords
from yt_sugg_que import main_function
from name_entity import name_entity_analysis
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.request import urlopen
import json


analyzer = SentimentIntensityAnalyzer()
key = Twitter_key.yt_key_shweta
#key = Twitter_key.yt_key


def extract_comments(videoId):
	commentExtractor = CommentExtractor()
	data = commentExtractor.get_video_comments(videoId)
	data.to_csv('sejal.csv')

	return data
 

def generate_keywords(comments_list):
	stops = list(set(stopwords.words('english') + ['&','i',')','(',',','.','view','add','know','use','blah','bla','available','appear','actually','arrive','come','cut','days','day','click','check','didnt','like','lot','need','new','place','watch','work','whats','want','video','cant','dont','fuck','view','add','know','use','blah','bla','available','appear','actually','arrive','come',
                  'cut','days','day','check','didnt','like','lot','need','new','place','watch','work',
                'whats','want','video','thing','look','see','everyone','each','see','look','grow','everything',
                 'everybody']))


	tokens = []
	for i in comments_list:		
		tokens.append(i.split())

	words = []
	words_freq=[]
	words_json=[]

	for i in tokens:
		for j in i:
			if len(j)>2:
				words.append(j) 

	words_freq = Counter(words)
	word_list = [word for word, count in words_freq.items()]


	word_bist = set(word_list)- set(stops)

	words_json = [{'text': word, 'value':int(count)} for word, count in words_freq.items() if word in word_bist]
	f = sorted(words_json, key =lambda x:x['value'], reverse=True)
	f = f[:50]
	return f


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

	#complete = neg + neu + pos
	neg_em = neg
	pos_em = pos
	neu_em = neu
	sentiment = [{ "x":'negative', 'y':neg_em },{'x':'positive','y':pos_em},{'x':'neutral', 'y':neu_em}]
	return sentiment


def youtube_user_video(channelId):
	result = {}
	latest_video_id =True # get_video_id(channelId)
	if latest_video_id != False:
		data = extract_comments('nkcKdfL7G3A')#latest_video_id) 
		stats = video_statistics('nkcKdfL7G3A')#latest_video_id)	

		suggestions, questions, personal, comments_list, raw_list = main_function(data, "youtube") 
	
		result['keywords'] = generate_keywords(comments_list)	
		result['questions']= questions
		result['suggestions']={'creator':personal, 'content': suggestions}
		result['sentiment_analysis'] = sentiment_analysis(comments_list)
		result['aspect_analysis'] = name_entity_analysis(raw_list)
		result['stats'] = stats
		print(result)
		return result

	else:
		return False, False


def video_statistics(videoId):
	source = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(videoId, key)
	response = urlopen(source)
	s = json.loads(response.read())

	result =[{ "heading": "likes", "count": s['items'][0]['statistics']['likeCount'] },
    { "heading": "dislikes", "count": s['items'][0]['statistics']['dislikeCount'] },
    { "heading": "views", "count": s['items'][0]['statistics']['viewCount'] },
    { "heading": "comments", "count": s['items'][0]['statistics']['commentCount'] }]

	return result 


def get_video_id(channelId):
	url ='https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults=1'.format(key, channelId)
	resp = urlopen(url)
	response = json.loads(resp.read()) 
	if response['items']!=[]:  
		videoId = response['items'][0]['id']['videoId']
		print()
		print("videoid", videoId)
		print()
		return videoId
	else:
		return False

