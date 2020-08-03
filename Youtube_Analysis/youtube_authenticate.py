import json
import httplib2
import http.client
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import random
from datetime import datetime
from urllib.request import urlopen
from oauth2client.file import Storage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser, run_flow
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from flask import Flask, request, redirect, session, url_for, render_template, jsonify


#youtube developer key
yt_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#import the json file in your developer account
CLIENT_SECRETS_FILE = "client_secret.json" 
#various permissions to ask from the user
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl', "https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/userinfo.profile", " https://www.googleapis.com/auth/youtube.upload", "openid"]
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
  http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def credentials_to_dict(credentials):
	return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def build_youtube(credentials):
	credentials = google.oauth2.credentials.Credentials(**credentials)
	youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
	return youtube


#get the statistics of any youtube channel given channel id
def youtube_info(channel_id, yt_key):
	source = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}'.format(channel_id, yt_key)
	response = urlopen(source)
	s = json.loads(response.read())
	return s

#function to redirect to the youtube authentication page
def add_youtube():
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	CLIENT_SECRETS_FILE, scopes=SCOPES)  
	flow.redirect_uri = url_for('callback', _external=True)
	authorization_url, state = flow.authorization_url(
	access_type='offline',
	include_granted_scopes='true')
	return authorization_url, state

#callback function that authenticates and grants permission for the various scopes
def youtube_callback(state):
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
	flow.redirect_uri = url_for('callback', _external=True)
	authorization_response = request.url
	flow.fetch_token(authorization_response=authorization_response)
	credentials = flow.credentials

	credentials = credentials_to_dict(credentials)
	credentials = google.oauth2.credentials.Credentials(
	**credentials)
	
	print(credentials.token)
	cred = {}
	cred["refresh_token"] = credentials.refresh_token
	cred["token"] = credentials.token
	cred["scopes"] = credentials.scopes
	cred["token_uri"] = credentials.token_uri
	cred["client_id"] = credentials.client_id
	cred["client_secret"] = credentials.client_secret
	return cred


#get the youtube stats
def extract_all_info(credentials):
	refresh_token = credentials['refresh_token']
	token = credentials['token']
	scopes = credentials["scopes"]

	#extract google id
	resp = urlopen("https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={}".format(token))
	info = json.loads(resp.read())
	
	youtube = build_youtube(credentials)
	channel = youtube.channels().list(mine=True, part='snippet').execute()

	s = youtube_info(channel['items'][0]['id'], yt_key)

	sub = s['items'][0]['statistics']['subscriberCount']
	view = s['items'][0]['statistics']['viewCount']
	video = s['items'][0]['statistics']['videoCount']
	return sub, view, video
		

#function to upload video on user channel
def youtube_upload(resp, channel_id, video):
	credentials = get_credentials(channel_id)
	youtube = build_youtube(credentials)
	body=dict(
	  snippet=dict(
	    title = resp["title"],
	    description = resp["description"],
	    tags = resp["tags"],
	    categoryId = resp["category"]
	  ),
	  status=dict(
	    privacyStatus='public'
	  )
	)
	insert_request = youtube.videos().insert(
	  part=",".join(body.keys()),
	  body=body, 
	  media_body=MediaFileUpload(video, chunksize=-1, resumable=True)
	)
	response = None
	error = None
	retry = 0
	while response is None:
		try:
			print("Uploading file...")
			status, response = insert_request.next_chunk()
			if response is not None:
				if 'id' in response:
					print("Video id '%s' was successfully uploaded." % response['id'])
					return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
			else:
			    exit("The upload failed with an unexpected response: %s" % response)
			    return json.dumps({'success':False}), 400, {'ContentType':'application/json'}
		except HttpError as e:
			if e.resp.status in RETRIABLE_STATUS_CODES:
				error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
						                  e.content)
			else:
				raise
		except (RETRIABLE_EXCEPTIONS, e):
			error = "A retriable error occurred: %s" % e
