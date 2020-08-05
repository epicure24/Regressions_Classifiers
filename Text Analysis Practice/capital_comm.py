from bs4 import BeautifulSoup
import pandas as pd

html_doc = open('caa.html', 'r+')
soup = BeautifulSoup(html_doc, 'html.parser')

data = pd.DataFrame()
comm_data = pd.DataFrame()

#data_old = pd.read_csv("caa_facebook.csv", engine="python")
comm_data_old = pd.read_csv("comments_capitals_facebook.csv", engine="python")

#page Name
'''for d in soup.find_all("div", attrs={'id':'objects_container'}):
	page_name = d.a.text
	print(page_name)'''


for d in soup.find_all("h3", attrs={'class':'bj bk bl bm'}):
	page_name = d.a.text
	print(d.a.text)
#post content
'''post_content =[]
for d in soup.find_all("div", attrs={'class':'bk'}):
	try:
		post_content.append(d.p.text)
		print(post_content)
	except:
		print("error")'''

#reactions
for d in soup.find_all("div", attrs={'class':'dd'}):
	reactions = d.text
	print(reactions)

comm_list =[]
data_list = []
#comments
for d in soup.find_all("div"):
	if d.get('id') != None and d.get('id').isdigit() == True:
		#user name
		user = d.a.text
		print("username", user)
		#comment
		try:
			comm_div = d.find('div', attrs={'class':'ej'})
			comment = comm_div.text
			print("comment" ,comment)
		except:
			comm_div = d.find('div', attrs={'class':'ef'})
			comment = comm_div.text
			print(comment)
		#likes
		like = d.find('a', attrs={'class':'eo cb'})
		try:
			likes = like.contents[1]
			print(likes)
		except:
			likes = 0
			print(likes)


		comm_list.append([user, comment, likes])

length = len(comm_list)
#data_list.append([page_name, post_content, reactions, length])

#data = data.append(data_list)
comm_data = comm_data.append(comm_list)

#data.columns=["page_name", "post_content", "reactions", "comments"]
comm_data.columns=["user","commentText","reactions"]

#data_old = (pd.concat([data, data_old], ignore_index=True, sort=False).reindex(columns=data_old.columns))
comm_data_old = (pd.concat([comm_data, comm_data_old], ignore_index=True, sort=False).reindex(columns=comm_data_old.columns))

#data_old.reset_index(drop=True, inplace=True)
comm_data_old.reset_index(drop=True, inplace=True)

comm_data_old.drop_duplicates(subset=['commentText', 'user'],inplace=True)

#data_old.drop(data_old.columns[data_old.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
comm_data_old.drop(comm_data_old.columns[comm_data_old.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)


#data.to_csv("caa_facebook.csv")
comm_data_old.to_csv("comments_capitals_facebook.csv")

print(len(comm_data_old))
