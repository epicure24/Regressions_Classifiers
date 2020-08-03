import requests
import base64
from requests_oauthlib import OAuth1 
import json
from ast import literal_eval
import pandas as pd
import re
import operator
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem import WordNetLemmatizer
from gensim.summarization import keywords
import json

#TWITTER DEVELOPER ACCOUNT GIVES BEARER TOKEN FOR AUTHENTICATION PURPOSES
bearer_token = xxxxxxxxxxxxxxxxxx
search_headers = {
    'Authorization': 'Bearer {}'.format(bearer_token)    
}

def bmp(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

def gen_data():
	#NO. OF TWITTER PAGES YOU WANT TO EXTRACT DATA FROM (MAX PAGE IS 100)
	max_pages=30
	count = 0
	data = pd.DataFrame({"TWEET_ID":[],"TWEET_TEXT":[],"HASHTAGS":[],"USER_NAME":[],
		              "USER_SCREENNAME":[], "USER_ID":[], "FAVORITE_COUNT":[],
		              "RETWEET_COUNT":[],"USER_LOCATION":[],"DATE":[],
		              "URL_IN_TWEET":[],"USER_MENTIONS":[],"CATEGORY":[]})

	#DIFFERENT CATEGORIES TO EXTRACT TWEETS 
	category_lis  = ['food','fashion','media','technologies','blog','travel','education','entertainment','photography']

	for category in category_lis:
		
		#URL FOR EXTRACTING TWEETS
		url ='https://api.twitter.com/1.1/search/tweets.json?q=%23'
		st = '%s'%category
		ht = '&lang=en&result_type=mixed&count=100'

		url = url + st + ht

		list_id =[]

		for i in range(0, max_pages):
			r = requests.get(url, headers=search_headers)
			url ='https://api.twitter.com/1.1/search/tweets.json?q=%23'
			st = '%s'%category
			ht = '&lang=en&result_type=mixed&count=100'

			url = url + st + ht   
			bytes_to_json = r.content.decode('utf-8')
			data_1 = json.loads(bytes_to_json)
			try:
			    
				for s in data_1['statuses']:
					s =str(s).encode('utf-8').decode('utf-8')
					s = bmp(s)
					s = literal_eval(s)
					list_id.append(s['id'])
					data=data.append({"TWEET_ID":s['id'],"TWEET_TEXT":s['text'],
							  "HASHTAGS":[i['text']for i in s['entities']['hashtags']],
							  "USER_NAME":s['user']['name'],
							  "USER_SCREENNAME":s['user']['screen_name'],
							  "USER_ID":s['user']['id'],"FAVORITE_COUNT":s['favorite_count'],
							  "RETWEET_COUNT":s['retweet_count'],"USER_LOCATION":s['user']['location'],
							  "DATE":s['created_at'],"URL_IN_TWEET":[i['url'] for i in s['entities']['urls']],
							  "USER_MENTIONS":s['entities']['user_mentions'],"CATEGORY":category},ignore_index=True)

				url = url + "&max_id={}".format(min(list_id)-1)
			except:
				continue

	#shuffle the dataset
	data = data.sample(frac=1)

	data.drop_duplicates(subset=['TWEET_TEXT'], inplace=True)
	data.dropna(subset=['TWEET_TEXT'], inplace=True)

	#PREPROCESSING OF THE DATA
	wnl = WordNetLemmatizer()

	stop_words = set(stopwords.words('english'))
	tweet_list =[]
	lemmatized_tokens =[]

	for index, row in data.iterrows():
		text = str(row['TWEET_TEXT']).encode('ascii','ignore').decode('UTF-8')
		text = re.sub(r"#",'',text)
		text = re.sub(r"RT @[\w]+:",'',text)
		text = re.sub(r"RT @[\w]+:",'',text)
		text = re.sub(r" RT ",'',text)
		text = re.sub(r"@","",text)
		text = re.sub(r"&amp","and",text)
		text = re.sub(r"https://[\w]+.[\w]+/[\w]+",'',text)
		text = re.sub(r"[][]",'',text)
		text = re.sub(r"[:/;}{)(=''!*,%]","",text)
		text = re.sub(r" - ",'',text)
		text = re.sub(r" _ ",'',text)
		text = re.sub(r"[.]",'',text)
		text = re.sub(r'[""]','',text)
		text = re.sub(r"[?]",'',text)
		tweet = text.strip()
		tweet = tweet.lower()

		tweet_list.append(tweet.lower())

		tokens = word_tokenize(str(tweet))
		tokens = [word for word in tokens if word not in stop_words]
		lems=[]
		kems =[]
		pems =[]
		stops = list(set(stopwords.words('english') + ['&','i',')','(',',','.','view','add','know','use','blah','bla','available','appear','actually','arrive','come','cut','days','day','click','check','didnt','like','lot','need','new','place','watch','work','whats','want','video']))
		#remove one-letter word
		tokens = [word for word in tokens if len(word)>1]
		#pos_tagging to choose noun only
		for i in pos_tag(tokens):
			if i[1].startswith('N'):
				kems.append(i[0])
	    
		for word, tag in pos_tag(kems):
			wntag = tag[0].lower()
			wntag = wntag if wntag in ['a','r','n','v'] else None
			if not wntag:
				lems.append(word)
			else:
				lems.append(wnl.lemmatize(word, wntag))
	    
	    
		for i in lems:
			if i not in stops:
				pems.append(i)

		lemmatized_tokens.append(pems)

	data["TOKENS"] = lemmatized_tokens
	
	#STORE TWEETS AFTER CLEANING
	data['CLEAN_TWEET'] = tweet_list

	
	#analysis of the twitter dataset

	fav_output = {"FOOD":0, "MEDIA":0, "TECHNOLOGY":0, "TRAVEL":0, "BLOG":0, "ENTERTAINMENT":0, "PHOTOGRAPHY":0, "FASHION":0,
		 "EDUCATION":0}

	ret_output = {"FOOD":0, "MEDIA":0, "TECHNOLOGY":0, "TRAVEL":0, "BLOG":0, "ENTERTAINMENT":0, "PHOTOGRAPHY":0, "FASHION":0,
		 "EDUCATION":0}

	time_int = {}

	#Category Wise Likes 
	foo =0
	med =0
	tec = 0
	tra = 0
	blo = 0
	ent = 0
	pho = 0
	fas = 0
	inf = 0

	for index, rows in data.iterrows():
		if rows["CATEGORY"] == 'food':
			foo += int(rows["FAVORITE_COUNT"])
		elif rows["CATEGORY"] == 'media':
			med += int(rows["FAVORITE_COUNT"])
		elif rows["CATEGORY"] == 'entertainment':
			ent += int(rows["FAVORITE_COUNT"])
		elif rows["CATEGORY"] == 'travel':
			tra += int(rows["FAVORITE_COUNT"])
		elif rows["CATEGORY"] == 'blog':
			blo += int(rows["FAVORITE_COUNT"])
		elif rows["CATEGORY"] == 'photography':
			ent += int(rows["FAVORITE_COUNT"])
		elif rows["CATEGORY"] == 'fashion':
			fas += int(rows["FAVORITE_COUNT"])
		elif rows["CATEGORY"] == 'education':
			inf += int(rows["FAVORITE_COUNT"])
		elif rows["CATEGORY"] == "technologies":
			tec += int(rows["FAVORITE_COUNT"])

	for key, value in fav_output.items():
		if key == "FOOD":
			fav_output.update({key:foo})
		elif key == "MEDIA":
			fav_output.update({key:med})
		elif key == "ENTERTAINMENT":
			fav_output.update({key:ent})
		elif key == "TRAVEL":
			fav_output.update({key:tra})
		elif key == "BLOG":
			fav_output.update({key:blo})
		elif key == "PHOTOGRAPHY":
			fav_output.update({key:pho})
		elif key == "FASHION":
			fav_output.update({key:fas})
		elif key == "TECHNOLOGY":
			fav_output.update({key:tec})
		elif key == "EDUCATION":
			fav_output.update({key:inf})

	output_data = {
	'categorywise_retweets':[],
	'categorywise_likes':[],
	'timewise_tweets':[], 
	'daywise_tweets':[],
	'categories':{}
	}


	#Category Wise Retweets

	foo =0
	med =0
	tec = 0
	tra = 0
	blo = 0
	ent = 0
	pho = 0
	fas = 0
	inf = 0

	for index, rows in data.iterrows():
		if rows["CATEGORY"] == 'food':
			foo += int(rows["RETWEET_COUNT"])
		elif rows["CATEGORY"] == 'media':
			med += int(rows["RETWEET_COUNT"])
		elif rows["CATEGORY"] == 'entertainment':
			ent += int(rows["RETWEET_COUNT"])
		elif rows["CATEGORY"] == 'travel':
			tra += int(rows["RETWEET_COUNT"])
		elif rows["CATEGORY"] == 'blog':
			blo += int(rows["RETWEET_COUNT"])
		elif rows["CATEGORY"] == 'photography':
			ent += int(rows["RETWEET_COUNT"]) 
		elif rows["CATEGORY"] == 'fashion':
			fas += int(rows["RETWEET_COUNT"])
		elif rows["CATEGORY"] == 'education':
			inf += int(rows["RETWEET_COUNT"])
		elif rows["CATEGORY"] == "technologies":
			tec += int(rows["RETWEET_COUNT"])

	for key, value in ret_output.items():
		if key == "FOOD":
			ret_output.update({key:foo})
		elif key == "MEDIA":
			ret_output.update({key:med})
		elif key == "ENTERTAINMENT":
			ret_output.update({key:ent})
		elif key == "TRAVEL":
			ret_output.update({key:tra})
		elif key == "BLOG":
			ret_output.update({key:blo})
		elif key == "PHOTOGRAPHY":
			ret_output.update({key:pho})
		elif key == "FASHION":
			ret_output.update({key:fas})
		elif key == "TECHNOLOGY":
			ret_output.update({key:tec})
		elif key == "EDUCATION":
			ret_output.update({key:inf})

	for i in fav_output.keys():
		output_data["categorywise_likes"].append({"x":i,"y":int(fav_output[i])})
		output_data["categorywise_retweets"].append({"x":i,"y":int(ret_output[i])})

	#daywise tweets
	#day_output ={"MONDAY":0, "TUESDAY":0, "WEDNESDAY":0, "THURSDAY":0, "FRIDAY":0, "SATURDAY":0, "SUNDAY":0}
	day_output ={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

	for index, rows in data.iterrows():
		date = str(rows["DATE"])
		date = date.split()[0].lower()
		if date == 'mon':
			day_output.update({0:day_output[0]+1})
		elif date == 'tue':
			day_output.update({1:day_output[1]+1})
		elif date == 'wed':
			day_output.update({2:day_output[2]+1})
		elif date == 'thu':
			day_output.update({3:day_output[3]+1})
		elif date == 'fri':
			day_output.update({4:day_output[4]+1})
		elif date == 'sat':
			day_output.update({5:day_output[5]+1})
		elif date == 'sun':
			day_output.update({6:day_output[6]+1})


	for i in day_output.keys():
		output_data["daywise_tweets"].append({"x":i,"y":int(day_output[i])})

	#Time Wise Tweets

	time_d = pd.DataFrame()
	time_lis =[]

	for index, rows in data.iterrows():
		time = str(rows["DATE"])
		time = time.split()
		if len(time) == 6:
			time = time[3][:2]
			time_lis.append(time)

	time_d["TIME"] = time_lis

	table = time_d["TIME"].value_counts()
	tab = []
	for i in table.keys():
		tab.append({"x":i,"y":int(table[i])})

	tab = sorted(tab, key= lambda x :x['x'])
	output_data['timewise_tweets'] = tab

	category_lis  = ['food','fashion','media','technologies','blog','travel','education','entertainment','photography']
#stop_words = set(stopwords.words('english'))

	unwanted_words = {'cant','dont','fuck','view','add','know','use','blah','bla','available','appear','actually','arrive','come',
                  'cut','days','day','check','didnt','like','lot','need','new','place','watch','work',
                'whats','want','video','thing','look','see','everyone','each','see','look','grow','everything',
                 'everybody'}

	for category in category_lis:
		df =  data[data['CATEGORY']== category]
		words = []
		words_freq=[]
		words_json=[]

		for i in df['TOKENS']:
			for j in i:
				if len(j)>2:
					words.append(j) 

		words_freq = Counter(words)
		word_list = [word for word, count in words_freq.items()]


		word_bist = set(word_list)- unwanted_words

		words_json = [{'text': word, 'value':int(count)} for word, count in words_freq.items() if word in word_bist]
		f = sorted(words_json, key =lambda x:x['value'], reverse=True)
		f = f[:50]
		output_data['categories'].update({category:{"keywords":f}})


		#print(output_data)
	    
		#hash_tags
		hashes = df['HASHTAGS']

		hash_list = []
		for i in hashes:
			i = str(i).encode('ascii','ignore').decode('UTF-8')
			i = re.sub(r'[,\']','',i)
			i = re.sub(r']','',i)
			i = re.sub(r'[][]','',i)
		for j in i.split():
			hash_list.append(j)

		hash_freq = Counter(hash_list)
		hash_json = [{'text': word, 'value': count} for word, count in hash_freq.items()]
		f = sorted(hash_json, key =lambda x:x['value'], reverse=True)
		f = f[:50]
		hash_tags = []
		for i in f:
			hash_tags.append(i["text"].lower())
			output_data['categories'][category]["hashtags"] = list(set(hash_tags))


	print(output_data)

	return output_data

