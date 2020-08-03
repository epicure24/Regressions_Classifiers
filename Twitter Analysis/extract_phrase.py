from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
import re
from nltk import pos_tag
from nltk.collocations import *

bigram_measures = nltk.collocations.BigramAssocMeasures()
#trigram_measures = nltk.collocations.TrigramAssocMeasures()


def gen_tok(lis):
	stop_words = stopwords.words('english') + ['i','I','look','like','but','each','everyone','everything','can','make','do','done',
	'does','could','would','please','video','review','plz','get','unbox','might','anyone','listen',
'watch','listening','watching']

	wnl = WordNetLemmatizer()

	tokens =[]
	for sent in lis:
		lems =[]
		tok = sent.lower().split()
		wok = []
		for i in tok:
			if i not in stop_words:
				wok.append(i)
		text = ' '.join(k for k in wok)
		text = re.sub(r"[.]",' ',text)
		text = re.sub(r"http?[://\w]+",' ',text)
		text = re.sub(r"[?,'.)(<>!#$]",'',text)
		for word, tag in pos_tag(text.split()):
			wntag = tag[0].lower()
			wntag = wntag if wntag in ['a','r','n','v'] else None
			if not wntag:
				lems.append(word)
			else:
				lems.append(wnl.lemmatize(word, wntag))

		for j in lems:
			if j not in ['hi','hey','click','bio','retweet','us','i','my','I','ve','ll','dint','the','this','that','do','can','oh','lol','omg','ill','damn','didnt','the','would','could','now']:
				if len(j)==1 and (j.isupper() == True or j.isdigit() == True):
					tokens.append(j.lower())
				if len(j) > 1:
					tokens.append(j.lower())
	

	return tokens


def gen_phrases(tokens):
	finder = BigramCollocationFinder.from_words(tokens)
	finder.apply_freq_filter(2)
	phrase = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:10]
	phrase_list =[]
	for i in phrase:
		string = i[0][0]+ ' '+ i[0][1]
		phrase_list.append(string)
	
	return phrase_list


def most_common(lis, phrase_list):
	mos =[]

	for i in lis:
		for j in phrase_list:
			if j in i:
				mos.append(i)
			sep = j.split()
			regex = '{} (\w)+ {}'.format(sep[0], sep[1])             
		    
			match = re.search(regex, i) 
			
			if match != None:
			    mos.append(i)
	
	return list(set(mos))


def gen_phrases_function(lis):
	tokens = gen_tok(lis)
	phrase_list = gen_phrases(tokens)

	sent_list = most_common(lis, phrase_list)
	return phrase_list, sorted(sent_list, key=lambda x: len(x))


'''lis = ["hey sanam, how are you", "your voice is so melodious sanam", "superb song of sanam",
"please sing another song sanam", "what will be your next song sanam"]

p, s = gen_phrases_function(lis)
print(p)
print(s)
freq = {}
for i in p:
	h = i.split()
	freq[i]=[]
	for j in s:
		if h[0] in j or h[1] in j:
			freq[i].append(j)

print(freq)'''
