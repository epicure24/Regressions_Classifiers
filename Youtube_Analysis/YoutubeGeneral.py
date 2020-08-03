import requests, sys, time, os, argparse
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from textblob import TextBlob
from collections import Counter

country_codes ={'US':'USA', 'IN':'India', 'BR':'Brazil', 'GB':'UK', 'TH':'Thailand', 'RU':'Russia', 'KR':'South Korea','ES':'Spain','JP':'Japan','CA':'Canada','AU':'Australia'}
#country_codes={'US':'USA', 'IN':'India','BR':'Brazil', 'GB':'UK'}


snippet_features = ["title",
                        "publishedAt",
                        "channelId",
                        "channelTitle",
                        "categoryId"]


unsafe_characters = ['\n', '"']

header = ["video_id"] + snippet_features + ["trending_date", "tags", "view_count", "likes", "dislikes",
                                                "comment_count", "thumbnail_link", "comments_disabled",
                                                "ratings_disabled", "description", "duration"] + ["country_code"]

def setup():
    yt_api_key = 'AIzaSyC5CsVkXU7Ch7ApqlyVyms5dkNNvDuSHnw' 

    #'AIzaSyAU7udU_6olfeXV5WOcuOi68VouR9PW2NU'
    yt_country_codes = country_codes
    return yt_api_key, yt_country_codes


def prepare_feature(feature):
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def api_request(page_token, country_code):
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,contentDetails,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=10&key={api_key}"
    request = requests.get(request_url)
    
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    
    return request.json()


def get_tags(tags_list):

    return prepare_feature("|".join(tags_list))

def get_videos(items,df, country_code):
    line = []
    for video in items:
        comments_disabled = False
        ratings_disabled = False
        
        if "statistics" not in video:
            continue


        video_id = prepare_feature(video['id'])

        
        snippet = video['snippet']
        statistics = video['statistics']
        contentDetails = video['contentDetails']

        
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]

        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y.%d.%m")
        tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = statistics.get("viewCount", 0)
        duration = contentDetails.get("duration", "")
        
        if 'likeCount' in statistics and 'dislikeCount' in statistics:
            likes = statistics['likeCount']
            dislikes = statistics['dislikeCount']
        else:
            ratings_disabled = True
            likes = 0
            dislikes = 0

        if 'commentCount' in statistics:
            comment_count = statistics['commentCount']
        else:
            comments_disabled = True
            comment_count = 0

        line = [video_id] + features + [prepare_feature(x) for x in [trending_date, tags, view_count, likes, dislikes,
                                                                       comment_count, thumbnail_link, comments_disabled,
                                                                       ratings_disabled, description, duration]]
        
        line.append(country_code)
        df = df.append({'video_id': line[0], 'title': line[1], 'publishedAt': line[2], 'channelId': line[3], 'channelTitle': line[4], 'categoryId': line[5],
                        'trending_date': line[6], 'tags': line[7], 'view_count': line[8], 'likes': line[9], 'dislikes': line[10],
                        "comment_count": line[11], "thumbnail_link": line[12], "comments_disabled": line[13],
                                            "ratings_disabled": line[14], "description": line[15], "duration": line[16], "country_code": line[17]
                                            }, ignore_index=True)


    return df


def get_pages(country_code, df, next_page_token="&"):

    country_data = []
    i = 1
    while next_page_token is not None:
        video_data_page = api_request(next_page_token, country_code)
    
        next_page_token = video_data_page.get("nextPageToken", None)
        
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token
        
        items = video_data_page.get('items', []) 
        df = get_videos(items,df,country_code)
        df.reset_index()
        i+=1
    return df


def get_data():
    print("data called")
    df =  pd.DataFrame(columns=header)
    for country_code in country_codes.keys():
        df = df.append(get_pages(country_code,df), ignore_index=True)
        df.drop_duplicates(inplace=True)
    return df


#global analysis function
def global_analysis(column, data):
    glo_dict = []
    df = data.groupby(['country_code'])[[column]].sum()
    x =df.sort_values(column, ascending= False).head()

    for index, rows in x.iterrows():
        glo_dict.append({"x":country_codes[index],"y":int(rows[column])})
        
    return glo_dict


#country_wise analysis function
def country_analysis(country_code, column, category_dict, data):
    con_dict =[]
    df = data[data['country_code']==country_code]
    df = df.groupby(['categoryId'])[[column]].sum()
    x = df.sort_values(column, ascending=False).head()
    
    for index, rows in x.iterrows():
        key = '%s'%index
        con_dict.append({'x':category_dict[key],'y':int(rows[column])})
      
    return con_dict

#country_wise hashtags
def country_hashtags(df):
    words =[]
    for i in df['hashtags']:
        for j in i:
            j=j.replace('"','')
            words.append(j)
    return words

def youtube_analysis():
    data = get_data()
    wnl = WordNetLemmatizer()

    stop_words = stopwords.words('english')

    lemmatized_tokens =[]
    for index, row in data.iterrows():
        #read_only_ascii
        text = str(row["description"]).encode("ascii", "ignore").decode("utf-8")
        #lowerCase_the_text
        text = text.lower()
        text = re.sub(r'[&)(://?.-]','',text)
        text = re.sub(r'http?[\w]+','',text)
        #remove mentions
        text = re.sub(r'@[\w]+','',text)
        #remove punctuations
        tokens = word_tokenize(str(text))
        tokens = [word for word in tokens if word not in stop_words]
        lems=[]
        #remove one-letter word
        tokens = [word for word in tokens if len(word)>1]
        for word, tag in pos_tag(tokens):
            wntag = tag[0].lower()
            wntag = wntag if wntag in ['a','r','n','v'] else None
            if not wntag:
                lems.append(word)
            else:
                lems.append(wnl.lemmatize(word, wntag))

        lemmatized_tokens.append(lems)

    data["tokens"] = lemmatized_tokens
    lis = []
    for i in data['tags']:
        lis.append(i.split('|'))

    data['hashtags']= lis
    
    #analysis code

    category_dict = {
    '"2"': "Autos & Vehicles",
    '"1"': "Film & Animation",
    '"10"' : "Music",
    '"15"' : "Pets & Animals",
    '"17"' : "Sports",
    '"18"' : "Short Movies",
    '"19"' : "Travel & Events",
    '"20"': "Gaming",
    '"21"' : "Videoblogging",
    '"22"': "People & Blogs",
    '"23"' : "Comedy",
    '"24"' : "Entertainment",
    '"25"' : "News & Politics",
    '"26"' : "Howto & Style",
    '"27"': "Education",
    '"28"' : "Science & Technology",
    '"29"': "Nonprofits & Activism",
    '"30"' : "Movies",
    '"31"': "Anime/Animation",
    '"32"' : "Action/Adventure",
    '"33"': "Classics",
    '"34"' : "Comedy",
    '"35"': "Documentary",
    '"36"' : "Drama",
    '"37"': "Family",
    '"38"' : "Foreign",
    '"39"': "Horror",
    '"40"' : "SciFi/Fantasy",
    '"41"': "Thriller",
    '"42"' : "Shorts",
    '"43"': "Shows",
    '"44"': "Trailers"
    }


    general ={"global":{}}


    like_lis=[]
    dislike_lis=[]
    view_lis=[]
    comment_lis =[]


    for i, r in data.iterrows():
        like_lis.append(int(r['likes'].replace('"', "")))
        dislike_lis.append(int(r['dislikes'].replace('"', "")))
        view_lis.append(int(r['view_count'].replace('"', "")))
        comment_lis.append(int(r['comment_count'].replace('"', "")))


    data['likes_count'] = like_lis
    data['dislikes_count'] = dislike_lis
    data['views']=view_lis
    data['comments']=comment_lis



    columns_list = ['likes_count','views','comments','dislikes_count']


    #global
    for i in columns_list:
        glo_dict = global_analysis(i, data)
        general["global"][i] = glo_dict

    #country_wise
    for country in country_codes.keys():
        country_output ={}
        for column in columns_list:
            con_dict = country_analysis(country, column, category_dict, data)
            country_output[column]=con_dict
            general.update({country_codes[country]:country_output})


    #global hashtags
    words =[]
    for i in data['hashtags']:
        for j in i:
            j=j.replace('"','')
            words.append(j)

    word_freq = Counter(words)
    words_json = [{'text': word, 'value':int(count)} for word, count in word_freq.items() if word!='[none]']
    f = sorted(words_json, key =lambda x:x['value'], reverse=True)
    f = f[:50]

    general['global'].update({'keywords':f})

    

    #country_wise hashtags
    for i in country_codes.keys():
        df = data[data['country_code']==i]
        words = country_hashtags(df)
        word_freq = Counter(words)
        words_json = [{'text': word, 'value':int(count)} for word, count in word_freq.items() if word!='[none]']
        f = sorted(words_json, key =lambda x:x['value'], reverse=True)
        f = f[:50]
        general[country_codes[i]].update({'keywords':f})

    #time duration analysis
    duration = data['duration']
    dictionary ={'0-1m':0, '1m-2m':0, '2m-5m':0, '5m-8m':0, '8m-10m':0, '10m-12m':0, '12m-15m':0, '20m-30m':0, '30m-45m':0, '45m-1h':0, 'hours':0}

    for i in duration:
        time = re.sub('PT','',i)

        #less than a minute video
        if time.find('H') == -1:
            if time.find('M')==-1:
                dictionary['0-1m']+=1
            else:
                time = re.sub(r'M[\w]*','',time)
                time = int(time.replace('"', ""))
                if time in range(1, 2):
                    dictionary['1m-2m']+=1
                elif time in range(2, 5):
                    dictionary['2m-5m']+=1
                elif time in range(5, 8):
                    dictionary['5m-8m']+=1
                elif time in range(8, 10):
                    dictionary['8m-10m']+=1
                elif time in range(10, 12):
                    dictionary['10m-12m']+=1
                elif time in range(12, 15):
                    dictionary['12m-15m']+=1
                elif time in range(20, 30):
                    dictionary['20m-30m']+=1
                elif time in range(30, 45):
                    dictionary['30m-45m']+=1
                elif time in range(45, 60):
                    dictionary['45m-1h']+=1
        else:
            time = re.sub(r'H[\w]+','',time)
            if time == '1':
                dictionary['45m-1h']+=1
            else:
                dictionary['hours']+=1

    general['global'].update({'Time_Duration':dictionary})

    #changing likes_count and dislikes_count into likes, dislikes
    general['global']['likes'] = general['global']['likes_count'] 
    general['global']['dislikes'] = general['global']['dislikes_count'] 
    
    del general['global']['likes_count']
    del general['global']['dislikes_count']

    for i in country_codes.keys():
        general[country_codes[i]]['likes'] = general[country_codes[i]]['likes_count']
        general[country_codes[i]]['dislikes'] = general[country_codes[i]]['dislikes_count']
        del general[country_codes[i]]['likes_count']
        del general[country_codes[i]]['dislikes_count']

    print(general)
    return general

api_key, country_codes = setup()


