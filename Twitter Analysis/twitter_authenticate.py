import requests
import Twitter_key
from requests_oauthlib import OAuth1Session, OAuth1
from urllib.request import urlopen
from urllib.parse import parse_qs, quote_plus
import json
from database_operations import check_twitter_details, save_twitter_details, update_twitter_details

request_url = "https://api.twitter.com/oauth/request_token"
auth_url = "https://api.twitter.com/oauth/authorize"
access_url = "https://api.twitter.com/oauth/access_token"
update_url = "http://api.twitter.com/1/statuses/update.json"

key = Twitter_key.consumer_key
secret = Twitter_key.consumer_secret

bearer_token =Twitter_key.bearer_token
search_headers = {
    'Authorization': 'Bearer {}'.format(bearer_token)    
}

def add_twitter():
	twitter = OAuth1Session(client_key= key, client_secret=secret)
	r = twitter.fetch_request_token(request_url)
	oauth_token = r["oauth_token"]
	oauth_secret = r["oauth_token_secret"]
	auth = twitter.authorization_url(auth_url)
	return oauth_token, oauth_secret, auth


def twitter_callback(token, oauth_secret, verifier, spear_id, email_id):
	twitter = OAuth1Session(key, client_secret=secret,                       resource_owner_key=token,resource_owner_secret=oauth_secret, verifier=verifier)
	response = twitter.fetch_access_token(access_url)
	access_token = response["oauth_token"]
	token_secret = response["oauth_token_secret"]
	a , t = check_twitter_details(response["user_id"])
	info = twitter_info(access_token, token_secret)

	print(info)

	if a == "no":
		save_twitter_details(access_token, token_secret, response["screen_name"],response["user_id"], spear_id, info, email_id)

	else:
		update_twitter_details(response["user_id"], response["screen_name"], info, email_id, access_token, token_secret)
	return "done"
	

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


def twitter_info(access_token, token_secret):

	twitter = OAuth1( client_key=key,
			client_secret=secret,
			resource_owner_key= access_token,
			resource_owner_secret= token_secret)

	url ='https://api.twitter.com/1.1/account/verify_credentials.json'
	resp = requests.get(url, auth=twitter)
	info = json.loads(resp.text)

	return info

