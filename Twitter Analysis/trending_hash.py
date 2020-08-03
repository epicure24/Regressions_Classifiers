import requests
import json
import Twitter_key

#database
import mysql.connector as ms
import time
from datetime import datetime

mydb = ms.connect(host="localhost", user ="root",passwd="shwetakrishnamohan", database="user_login")
mycursor = mydb.cursor(buffered=True)

access_token =Twitter_key.bearer_token
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}

def get_trending_hashtags(id):
	url = "https://api.twitter.com/1.1/trends/place.json?id={}&count=100".format(id)
	resp = requests.get(url, headers=search_headers)
	trends = json.loads(resp.text)
	trends_list =[]
	for trend in trends[0]['trends']:
		keys = trend['name']
		
		if keys.startswith("#"):
			trends_list.append(trend['name'].strip("#"))
		#else:
			#trends_list.append(trend['name'])
	return trends_list


def trends():
	countries = {'world': [{'city': 'Worldwide', 'woeid': 1}],
          'United Kingdom': [{'city': 'Birmingham', 'woeid': 12723},
	  {'city': 'Cardiff', 'woeid': 15127},
	  {'city': 'Derby', 'woeid': 18114},
	  {'city': 'Edinburgh', 'woeid': 19344},
	  {'city': 'Glasgow', 'woeid': 21125},
	  {'city': 'Liverpool', 'woeid': 26734},
	  {'city': 'Manchester', 'woeid': 28218},
	  {'city': 'Newcastle', 'woeid': 30079},
	  {'city': 'Nottingham', 'woeid': 30720},
	  {'city': 'London', 'woeid': 44418}],
	 'Mexico': [{'city': 'Mexico City', 'woeid': 116545},
          {'city': 'Acapulco', 'woeid': 110978},
          {'city': 'Guadalajara', 'woeid': 124162},
          {'city': 'Puebla', 'woeid': 137612},
	  {'city': 'Aguascalientes', 'woeid': 111579},
	  {'city': 'Chihuahua', 'woeid': 115958},
	  {'city': 'Ciudad Juarez', 'woeid': 116556},
	  {'city': 'Nezahualcóyotl', 'woeid': 116564},
	  {'city': 'Culiacán', 'woeid': 117994},
	  {'city': 'Ecatepec de Morelos', 'woeid': 118466},
	  {'city': 'Hermosillo', 'woeid': 124785},
	  {'city': 'León', 'woeid': 131068},
	  {'city': 'Mérida', 'woeid': 133327},
	  {'city': 'Mexicali', 'woeid': 133475},
	  {'city': 'Monterrey', 'woeid': 134047},
	  {'city': 'Morelia', 'woeid': 134091},
	  {'city': 'Naucalpan de Juárez', 'woeid': 134395},
	  {'city': 'Querétaro', 'woeid': 138045},
	  {'city': 'Saltillo', 'woeid': 141272},
	  {'city': 'San Luis Potosí', 'woeid': 144265},
	  {'city': 'Tijuana', 'woeid': 149361},
	  {'city': 'Toluca', 'woeid': 149769},
	  {'city': 'Zapopan', 'woeid': 151582},
	  {'city': 'Mexico', 'woeid': 23424900}],
          'Australia': [{'city': 'Perth', 'woeid': 1098081},
          {'city': 'Adelaide', 'woeid': 1099805},
          {'city': 'Brisbane', 'woeid': 1100661},
          {'city': 'Canberra', 'woeid': 1100968},
          {'city': 'Darwin', 'woeid': 1101597},
          {'city': 'Melbourne', 'woeid': 1103816},
          {'city': 'Sydney', 'woeid': 1105779}],
	 'India': [{'city': 'Mumbai', 'woeid': 2295411},
	  {'city': 'Pune', 'woeid': 2295412},
	  {'city': 'Hyderabad', 'woeid': 2295414},
	  {'city': 'Bangalore', 'woeid': 2295420},
	  {'city': 'Chennai', 'woeid': 2295424},
	  {'city': 'Delhi', 'woeid': 20070458},
          {'city': 'Kolkata', 'woeid': 2295386},
          {'city': 'Ahmedabad', 'woeid': 2295402},
          {'city': 'Nagpur', 'woeid': 2282863},
	  {'city': 'Lucknow', 'woeid': 2295377},
	  {'city': 'Kanpur', 'woeid': 2295378},
	  {'city': 'Patna', 'woeid': 2295381},
	  {'city': 'Ranchi', 'woeid': 2295383},
	  {'city': 'Srinagar', 'woeid': 2295387},
	  {'city': 'Amritsar', 'woeid': 2295388},
	  {'city': 'Jaipur', 'woeid': 2295401},
	  {'city': 'Rajkot', 'woeid': 2295404},
	  {'city': 'Surat', 'woeid': 2295405},
	  {'city': 'Bhopal', 'woeid': 2295407},
	  {'city': 'Indore', 'woeid': 2295408},
	  {'city': 'Thane', 'woeid': 2295410},
	  {'city': 'India', 'woeid': 23424848}],
	 'United States': [{'city': 'New York', 'woeid': 2459115},
          {'city': 'San Francisco', 'woeid': 2487956},
          {'city': 'Chicago', 'woeid': 2379574},
          {'city': 'Los Angeles', 'woeid': 2442047},
          {'city': 'Seattle', 'woeid': 2490383},
          {'city': 'Washington', 'woeid': 2514815},
          {'city': 'Boston', 'woeid': 2367105},
          {'city': 'Detroit', 'woeid': 2391585},
          {'city': 'Albuquerque', 'woeid': 2352824},
	  {'city': 'Atlanta', 'woeid': 2357024},
	  {'city': 'Austin', 'woeid': 2357536},
	  {'city': 'Baltimore', 'woeid': 2358820},
	  {'city': 'Baton Rouge', 'woeid': 2359991},
	  {'city': 'Birmingham', 'woeid': 2364559},
	  {'city': 'Charlotte', 'woeid': 2378426},
	  {'city': 'Cincinnati', 'woeid': 2380358},
	  {'city': 'Cleveland', 'woeid': 2381475},
	  {'city': 'Colorado Springs', 'woeid': 2383489},
	  {'city': 'Columbus', 'woeid': 2383660},
	  {'city': 'Dallas-Ft. Worth', 'woeid': 2388929},
	  {'city': 'Denver', 'woeid': 2391279},
	  {'city': 'El Paso', 'woeid': 2397816},
	  {'city': 'Fresno', 'woeid': 2407517},
	  {'city': 'Greensboro', 'woeid': 2414469},
	  {'city': 'Harrisburg', 'woeid': 2418046},
	  {'city': 'Honolulu', 'woeid': 2423945},
	  {'city': 'Houston', 'woeid': 2424766},
	  {'city': 'Indianapolis', 'woeid': 2427032},
	  {'city': 'Jackson', 'woeid': 2428184},
	  {'city': 'Jacksonville', 'woeid': 2428344},
	  {'city': 'Kansas City', 'woeid': 2430683},
	  {'city': 'Las Vegas', 'woeid': 2436704},
	  {'city': 'Long Beach', 'woeid': 2441472},
	  {'city': 'Louisville', 'woeid': 2442327},
	  {'city': 'Memphis', 'woeid': 2449323},
	  {'city': 'Mesa', 'woeid': 2449808},
	  {'city': 'Miami', 'woeid': 2450022},
	  {'city': 'Milwaukee', 'woeid': 2451822},
	  {'city': 'Minneapolis', 'woeid': 2452078},
	  {'city': 'Nashville', 'woeid': 2457170},
	  {'city': 'New Haven', 'woeid': 2458410},
	  {'city': 'New Orleans', 'woeid': 2458833},
	  {'city': 'Norfolk', 'woeid': 2460389},
	  {'city': 'Oklahoma City', 'woeid': 2464592},
	  {'city': 'Omaha', 'woeid': 2465512},
	  {'city': 'Orlando', 'woeid': 2466256},
	  {'city': 'Philadelphia', 'woeid': 2471217},
	  {'city': 'Phoenix', 'woeid': 2471390},
	  {'city': 'Pittsburgh', 'woeid': 2473224},
	  {'city': 'Portland', 'woeid': 2475687},
	  {'city': 'Providence', 'woeid': 2477058},
	  {'city': 'Raleigh', 'woeid': 2478307},
	  {'city': 'Richmond', 'woeid': 2480894},
	  {'city': 'Sacramento', 'woeid': 2486340},
	  {'city': 'St. Louis', 'woeid': 2486982},
	  {'city': 'Salt Lake City', 'woeid': 2487610},
	  {'city': 'San Antonio', 'woeid': 2487796},
	  {'city': 'San Diego', 'woeid': 2487889},
	  {'city': 'San Jose', 'woeid': 2488042},
	  {'city': 'Tallahassee', 'woeid': 2503713},
	  {'city': 'Tampa', 'woeid': 2503863},
	  {'city': 'Tucson', 'woeid': 2508428},
	  {'city': 'Virginia Beach', 'woeid': 2512636},
	  {'city': 'United States', 'woeid': 23424977}]}

	count_id = {'United States':23424977, 'United Kingdom':23424975 ,'Mexico':23424900, 'Australia':23424748, 'India':23424848}

	atlas ={'global':{'world':[],'United States':[],'United Kingdom':[],'India':[],'Mexico':[],'Australia':[]},'United States':{}, 'United Kingdom':{}, 'India':{}, 'Mexico':{}, 'Australia':{}}

	for key in countries:
		for i in countries[key][:10]:
			if key == 'world':
				atlas['global']['overall'] = get_trending_hashtags(1)
			else:
				atlas[key][i['city']] = get_trending_hashtags(i['woeid'])

	for key in count_id:
		atlas['global'][key] = get_trending_hashtags(count_id[key])

	'''sql_for = "insert into trends (date,time,trending_list) values (%s, %s, %s)"

	user = (datetime.now().strftime("%d-%h-%Y"), datetime.now().strftime("%H:%M:%S"), json.dumps(out))
	mycursor.execute(sql_for, user)
	mydb.commit()'''


	return atlas


out  = trends()
print(out)
sql_for = "insert into trends (date,time,trending_list) values (%s, %s, %s)"

user = (datetime.now().strftime("%d-%h-%Y"), datetime.now().strftime("%H:%M:%S"), json.dumps(out))
mycursor.execute(sql_for, user)
mydb.commit()



