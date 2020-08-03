import requests
import Twitter_key
from requests_oauthlib import OAuth1Session, OAuth1
from urllib.request import urlopen
from urllib.parse import parse_qs, quote_plus
import json

#various urls for twitter authentication
request_url = "https://api.twitter.com/oauth/request_token"
auth_url = "https://api.twitter.com/oauth/authorize"
access_url = "https://api.twitter.com/oauth/access_token"
update_url = "http://api.twitter.com/1/statuses/update.json"

key = #add consumer key here from developer account
secret = #add consumer secret key here from the twitter developer account

bearer_token = #insert bearer token from the twitter developer account
search_headers = {
    'Authorization': 'Bearer {}'.format(bearer_token)    
}

#call this function on the route , it will direct you to the twitter authentication page
def add_twitter():
	twitter = OAuth1Session(client_key= key, client_secret=secret)
	r = twitter.fetch_request_token(request_url)
	oauth_token = r["oauth_token"]
	oauth_secret = r["oauth_token_secret"]
	auth = twitter.authorization_url(auth_url)
	return oauth_token, oauth_secret, auth

#this function will returns the access tokens of the authentication of the user 
def twitter_callback(token, oauth_secret, verifier, spear_id, email_id):
	twitter = OAuth1Session(key, client_secret=secret,                       resource_owner_key=token,resource_owner_secret=oauth_secret, verifier=verifier)
	response = twitter.fetch_access_token(access_url)
	access_token = response["oauth_token"]
	token_secret = response["oauth_token_secret"]
	a , t = check_twitter_details(response["user_id"])
	info = twitter_info(access_token, token_secret)

	print(info)
	return "done"
	
#this function will return the basic info like screenname, name and profile data of the user
def twitter_info(access_token, token_secret):

	twitter = OAuth1( client_key=key,
			client_secret=secret,
			resource_owner_key= access_token,
			resource_owner_secret= token_secret)

	url ='https://api.twitter.com/1.1/account/verify_credentials.json'
	resp = requests.get(url, auth=twitter)
	info = json.loads(resp.text)

	return info

#This function will post the tweet on the user account using his access tokens and your developer keys.
def twitter_upload(text, access_token, access_token_secret):
	twitter = OAuth1(client_key = key, 
                        client_secret = secret,
                        resource_owner_key= access_token,
                        resource_owner_secret= access_token_secret
                        )

	status = quote_plus(text)
	url ='https://api.twitter.com/1.1/statuses/update.json?status={}'.format(status)
	resp = requests.post(url, auth=twitter)
	if "errors" in json.loads(resp.text):
		return {'success':False}
	else:
		return {'success':True}



