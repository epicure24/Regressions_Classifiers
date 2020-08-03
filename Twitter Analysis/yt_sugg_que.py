#youtube suggestions

from nltk import pos_tag, word_tokenize
import pandas as pd
import re
from extract_phrase import gen_phrases_function as gnf


suggestion_keys = ['review','react ','do a video','do video','make video','make a video','do reaction','reaction video','next video','unbox','upload','make a review','make review','do review','do a review','made a video', 'made video']

question_keys = ['is ','are ','do ','does ','would ','have ','has ','had ','should ','whose ','whom ','what ', 'why ','how ','where ','can ','could ','whose ','should ','will ','shall ','which ']

personal_suggestion_keys = ['you should ',"you shouldn't ","you shouldnt ", 'you must', 'suggest', 'recommend', 'you ought to']

#extract suggestions function

def extract_sugg_que(data, pur):
	comments_list = []
	raw_list = []
	if pur == 'yt':
		for index, rows in data.iterrows():
			text = str(rows['commentText']).encode("ascii", "ignore").decode("utf-8")
			#text = re.sub(r'http?[://\w]+','',text)
			text = re.sub(r'@[\w]+','',text)
			text = re.sub(r'\n','',text)
			comments_list.append(text)
			raw_list.append(text)
	else:
		comments_list = data
		raw_list = data

	suggestions = []
	questions = []
	personal_suggestions =[]

	for i in comments_list:
		text = " " + i + " "
		text = re.sub(r" pls",' please ', text)
		text = re.sub(r" pleas", ' please', text)
		text = re.sub(r" plz",' please', text)
		text = re.sub(r" e ",'', text)
		i = text.strip()
		for j in suggestion_keys:
			if j in i.lower():
				suggestions.append(i)
		for k in question_keys:
			if('?' in i or i.lower().startswith(k) or 'please reply' in i.lower()) and 'http' not in i and i not in suggestions:
				questions.append(i)

		for l in personal_suggestion_keys:
			if l in i.lower() and i not in suggestions and i not in questions:
				personal_suggestions.append(i)
	
	suggestions = list(set(suggestions))
	questions = list(set(questions))
	personal_suggestions = list(set(personal_suggestions))
	
	return suggestions, questions, personal_suggestions, comments_list, raw_list
	

def cleaning(lis):
	new = []
	for sent in lis:
		#lowercase
		text = sent.lower()
		#change certain things
		text = " " + text + " "
		#remove dots
		#text = re.sub(r"[.]",' ',text)
		text = re.sub(r" u ",' you ',text)
		text = re.sub(r" ur ",' your ',text)
		text = re.sub(r" pls",' please', text)
		text = re.sub(r" y ", ' why ', text)
		text = re.sub(r" plz",' please', text)
		text = re.sub(r" e ",'', text)
		text = re.sub(r" i'll ",' i will ',text)
		text = re.sub(r" we'll ",' we will ',text)
		text = re.sub(r" they'll ",' they will ',text)
		text = re.sub(r" you'll ",' you will ',text)
		text = re.sub(r" i'm ",' am ',text)

		#not
		text = re.sub(r" don't ",' do not ',text)
		text = re.sub(r" dont ",' do not ',text)
		text = re.sub(r" won't ",' will not ',text)
		text = re.sub(r" wont ",' will not ',text)
		text = re.sub(r" hasn't ",' has not ',text)
		text = re.sub(r" hasnt ",' has not ',text)
		text = re.sub(r" hadn't ",' had not ',text)
		text = re.sub(r" hadnt ",' had not ',text)
		text = re.sub(r" can't ",' can not ',text)
		text = re.sub(r" cant ",' can not ',text)
		text = re.sub(r" couldn't ",' could not ',text)
		text = re.sub(r" couldnt ",' could not ',text)
		text = re.sub(r" wouldn't ",' would not ',text)
		text = re.sub(r" wouldnt ",' would not ',text)
		text = re.sub(r" shan't ",' shall not ',text)
		text = re.sub(r" shouldn't ",' should not ',text)
		text = re.sub(r" shouldnt ",' should not ',text)
		text = re.sub(r" mightn't ",' might not ',text)
		text = re.sub(r" mightnt ",' might not ',text)
		text = re.sub(r" mustn't ",' must not ',text)
		text = re.sub(r" musnt ",' must not ',text)
		text = re.sub(r" doesnt ",' does not ',text)
		text = re.sub(r" didnt ",' did not ',text)
		text = re.sub(r" doesn't ",' does not ',text)
		text = re.sub(r" didn't ",' did not ',text)
		text = re.sub(r" weren't ",' were not ',text)
		text = re.sub(r" werent ",' were not ',text)
		text = re.sub(r" weren' ",' were not ',text)
		text = re.sub(r" wasn't ",' was not ',text)
		text = re.sub(r" wasn' ",' was not ',text)
		text = re.sub(r" wasnt ",' was not ',text)
		text = re.sub(r" needn't ",' need not ',text)
		text = re.sub(r" neednt ",' need not ',text)
		text = re.sub(r" needn' ",' need not ',text)
		text = re.sub(r" isn't ",' is not ',text)
		text = re.sub(r" aren't ",' are not ',text)
		text = re.sub(r" arent ",' are not ',text)
		text = re.sub(r" aint ",' are not ',text)
		text = re.sub(r" isn' ",' is not ',text)
		text = re.sub(r" ain' ",' are not ',text)
		text = re.sub(r" didn' ",' did not ',text)
		text = re.sub(r" don' ",' do not ',text)
		text = re.sub(r" doesn' ",' does not ',text)
		text = re.sub(r" couldn' ",' could not ',text)
		text = re.sub(r" wouldn' ",' would not ',text)
		text = re.sub(r" mightn' ",' might not ',text)
		text = re.sub(r" shouldn' ",' should not ',text)
		text = re.sub(r" mustn' ",' must not ',text)
		text = re.sub(r" hadn' ",' had not ',text)
		text = re.sub(r" hasn' ",' has not ',text)

		#have		
		text = re.sub(r" could've ",' could have ',text)
		text = re.sub(r" should've ",' should have ',text)
		text = re.sub(r" would've ",' would have ',text)
		text = re.sub(r" might've ",' might have ',text)
		text = re.sub(r" you've ",' you have ',text)
		text = re.sub(r" we've ",' we have ',text)
		text = re.sub(r" i've ",' you have ',text)

		#are
		text = re.sub(r" youre ",' you are ',text)
		text = re.sub(r" you're ",' you are ',text)
		text = re.sub(r" we're ",' we are ',text)
		text = re.sub(r" they're ",' they are ',text)
		text = re.sub(r" who're ",' who are ',text)

		text = re.sub(r" whats ",' what is ',text)
		text = re.sub(r" i ", ' I ', text)
		text = re.sub(r" [\w]*'ve ",' have ',text)
		text = re.sub(r" ive ",' i have ',text)
		text = re.sub(r" its ",' it is ',text)
		text = re.sub(r" it's ",'it is',text)
		text = re.sub(r" bro ",' brother ',text)
		text = re.sub(r" sis ",' sister ',text)
		text = re.sub(r' im ', ' i am ', text)
		text = re.sub(r" i'd ",'i would',text)
		text = re.sub(r" r ",' are ',text)
		text = re.sub(r" gonna ",' going to ',text)
		text = re.sub(r" wanna ",' want to ',text)
		text = re.sub(r" tis ",' this ',text)
		text = re.sub(r" any one ",' anyone ',text)
		text = text.strip()
		new.append(text)

	return new


def get_suggestions(suggestions):
	new = cleaning(suggestions)

	final = []
	kinal =[]
	please =[]
	keys =[' make video',' do video',' make review',' do review', ' make react', ' do react', ' made video',' make a video',' do a video',' make a review',' do a review',' make a react', ' do a react', ' made a video']
	for sent in new:
		text = sent
		text = " " + text + " "
		for i in keys:
			if i in text:
			    
				final.append(text.strip())
			    
		if (text.startswith('unbox ') or text.startswith('upload ') or text.startswith('react ')):# and len(text)<=100:

			kinal.append(text.strip())

		if (text.startswith('please ') or 'please' in text):

			please.append(text.strip())

	fin_sug =[]
	fsugg = list(set(final + kinal + please))
	for i in fsugg:
		if 'subscribe ' in i or 'click ' in i or 'bio ' in i:
			continue 
		else:
			fin_sug.append(i)

	return sorted(fin_sug, key= lambda x : len(x)) 


def get_questions(questions):
	new = cleaning(questions)

	filtered_sugg =[]
	quello =[]

	#first filter
	for i in new:
		if '?' in i and not i.lower().startswith('who') and not i.lower().startswith('anyone '):
			quello.append(i)

	suello = list(set(new)-set(quello))

	trash =[]
	kuello =[]

	for i in suello:

		if i.startswith('why'):
		
			kuello.append(i)

		tags = pos_tag(i.split())
		

		if (tags[0][1] =='VBZ' or tags[0][1] =='MD') and tags[1][1] == 'PRP':
			kuello.append(i)
		

		if tags[0][0] == 'what' and (tags[1][1] == 'VBZ' or tags[1][1] == 'NN'):
			kuello.append(i) 

		if tags[0][0].lower()== 'how':
			kuello.append(i)


		if tags[0][0].lower()== 'does':
			kuello.append(i)

		if tags[0][0] == 'why': #and (tags[1][1] == 'VBZ' or tags[1][1] == 'DT'):
			kuello.append(i)

		if tags[0][1].startswith('V') and tags[1][1] == 'PRP':
			kuello.append(i)

		if tags[0][0] == 'do' and (tags[1][1] != 'PRP'):
			filtered_sugg.append(i)
			suello.remove(i)

		if tags[0][0] == 'can' and (tags[1][1].startswith('V') or tags[1][1] == 'PRP') and (
		tags[1][0] not in ['look ','see ','relate ']):
		
			kuello.append(i)


		if tags[0][1].startswith('W') and tags[1][1] == 'MD':

			kuello.append(i)

		if tags[0][1].startswith('W') and tags[1][1].startswith('V') and 'who' not in i.lower():

			kuello.append(i)

		if tags[0][1].startswith('W') and tags[1][1] == 'PRP' and (i.lower().startswith('what') or i.lower().startswith('why') or i.lower().startswith('how')):
			
			kuello.append(i)


	kuello = list(set(kuello))

	#second filter
	trash = list(set(suello) - set((kuello + quello)))



	for i in trash:
		if i.startswith('how'):
			kuello.append(i)

		if i.startswith('why'):
			kuello.append(i)

		if 'would love to see' in i:
			kuello.append(i)

		tags = pos_tag(i.split())

		if tags[0][0] == 'can' and (tags[1][1].startswith('V') or tags[1][1] == 'PRP') and (
		tags[1][0] not in ['look ','see ','relate ']):
		
			kuello.append(i)

		if tags[0][0] =='what' and tags[1][0] == 'you':
			kuello.append(i)

		if tags[0][0] =='what' and tags[1][0] == 'is':
			kuello.append(i)    

		if tags[0][0] == 'which':
			kuello.append(i)

	fque = kuello + quello

	#third filter
	final_question_list = []

	for i in fque:
		if 'subscribe ' in i or 'click ' in i or 'bio ' in i:
			continue   
		if not i.startswith('who') and not ('anyone' in i or 'watching' in i or 'listening' in i) and i != '' and len(i.split())>4:
			final_question_list.append(i)


	return sorted(final_question_list, key= lambda x : len(x)) 

def get_personal(pers):
	sugg = cleaning(pers)
	psugg = []
	for i in sugg:
		if 'subscribe ' in i or 'click ' in i or ' bio ' in i:
			continue 
		else:
			psugg.append(i)

	return sorted(psugg, key= lambda x : len(x)) 

def main_function(data, platform):
	sugg, que, pers, comments_list, raw_list = extract_sugg_que(data,'yt')
	suggestions = get_suggestions(sugg)
	questions = get_questions(que)
	personal_suggestions = get_personal(pers)

	if platform == "hashtag":
		sugg, que, pers, comments_list, raw_list = extract_sugg_que(data, 'yt')
		suggestions = get_suggestions(sugg)
		questions = get_questions(que)
		personal_suggestions = get_personal(pers)

		return suggestions, questions, personal_suggestions, comments_list

	elif platform == "twitter":

		sugg, que, pers, comments_list, raw_list = extract_sugg_que(data, 'tw')
		suggestions = get_suggestions(sugg)
		questions = get_questions(que)
		personal_suggestions = get_personal(pers)

		sugge = suggestions + personal_suggestions
		sug ={'overall':sugge}
		phrase, mq = gnf(sugge)

		freq = {}
		for i in phrase:
			h = i.split()
			freq[i]=[]
			for j in mq:
				if h[0] in j or h[1] in j:
					freq[i].append(j)

		sug['frequent']= freq

		que ={'overall':questions}
		phrase, mq = gnf(questions)

		freq = {}
		for i in phrase:
			h = i.split()
			freq[i]=[]
			for j in mq:
				if h[0] in j or h[1] in j:
					freq[i].append(j)

		que['frequent']= freq


		return sug, que

	else:
		sug ={'overall':suggestions}
		phrase, mq = gnf(suggestions)

		freq = {}
		for i in phrase:
			h = i.split()
			freq[i]=[]
			for j in mq:
				if h[0] in j or h[1] in j:
					freq[i].append(j)

		sug['frequent']= freq

		que ={'overall':questions}
		phrase, mq = gnf(questions)

		freq = {}
		for i in phrase:
			h = i.split()
			freq[i]=[]
			for j in mq:
				if h[0] in j or h[1] in j:
					freq[i].append(j)

		que['frequent']= freq


		pers ={'overall':personal_suggestions}
		phrase, mq = gnf(personal_suggestions)

		freq = {}
		for i in phrase:
			h = i.split()
			freq[i]=[]
			for j in mq:
				if h[0] in j or h[1] in j:
					freq[i].append(j)

		pers['frequent']= freq
		
		return sug, que, pers, cleaning(comments_list), raw_list



#data = pd.read_csv('Test.csv', engine="python")

#s, q, p = main_function(data)

	
