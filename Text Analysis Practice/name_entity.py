from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
import pandas as pd
import re
import itertools
import en_core_web_sm
from collections import Counter

vader = SentimentIntensityAnalyzer()


nlp = en_core_web_sm.load()


def name_entity_analysis(comments_list):

	doc =[]
	for i in comments_list:
		doc.append(nlp(i))
	trial = []
	trial_item = []
	for i in range(0,len(doc)):
		trial.append([(X.text, X.label_) for X in doc[i].ents])

	trial = [x for x in trial if x != []]

	for i in trial:
		for item in i:
			if item[1] != "" and item[1] not in ["ORDINAL","DATE","CARDINAL","TIME","QUANTITY","PERCENT","LANGUAGE","MONEY"]:
				trial_item.append(item)


	counts = Counter(x[0] for x in trial_item)

	entities = sorted(counts.items(), key=lambda x: x[1], reverse = True)[0:10]

	sentiments = []

	for sentences in comments_list:
		for ele, ele1 in entities:
			if(ele in sentences):
				sentiments.append((ele, vader.polarity_scores(sentences)))

	top_entity = []
	for i in entities:
		top_entity.append(i[0])

	output =[]
	for j in top_entity:
		neg=0
		pos=0
		neu=0
		count =0
		for i in sentiments:
			if i[0] == j:
				count+=1
				neg+= i[1]['neg']
				pos+= i[1]['pos']
				neu+= i[1]['neu']
		analysis = {'neg':round((neg/count)*100),'pos':round((pos/count)*100),'neu':round((neu/count)*100)}
		total = round(analysis['neu'])+round(analysis['pos'])+round(analysis['neg'])
		if total < 100:
			diff = 100-total
			analysis['pos']+=diff
		elif total >100:
			diff = total-100
			analysis['neu']-=diff 
		output.append({'aspect':j, 'analysis':analysis}) 

	return output
