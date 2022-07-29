GOOGLE_API_KEY = "AIzaSyBPNwMqyOrYwifDTP72TIv841dTJdYqw4Q"
# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import threading
import csv



os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "desktop_secret.json"
topics = ["Ethnicity", "corruption", "Nigeria is not working", "constitution", "constitutionalism", "1999 constitution", "Nigerian constitution", "rule of law", "justice", "exclusive list", "concurrent list", "separation of power", "peace", "security", "law and order", "insecurity", "insurgency", "security votes"]
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
def scrape_youtube(topic, basepath):
   #  # Get credentials and create an API client
   #  flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
   #      client_secrets_file, scopes)
   #  credentials = flow.run_console()
    print(f'printing runinning {topic}')
    results = []
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=GOOGLE_API_KEY)

    request = youtube.search().list(
        q=topic,
        maxResults=50,
        part="snippet",
        type="video"
    )
    res = request.execute()
   
    results = results + res["items"]
    
    while "nextPageToken" in res:
      newrequest = youtube.search().list(
         q=topic,
         part="snippet",
         maxResults=50,
         type="video",
         pageToken=res["nextPageToken"],
      )
      res = newrequest.execute()
      results = results + res["items"]
    header = ["title", "link", "channelId", "date"]

    file = open(f'{basepath}/youtube-{topic}.csv', "w")
    writter = csv.writer(file)
    writter.writerows(header)
    writetofile(results, writter=writter)
    
def scrapeThreadhing():
   ts = []
   basepath = f'new/youtube'
   for topic in topics:
    #   query = f'{topic} since:2020-01-01'
      t = threading.Thread(target=scrape_youtube, args=(topic, basepath))
      t.start()
      ts.append(t)
   print("Waiting for threads to end")
   for t in ts:
      t.join()
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    scrapeThreadhing()
def writetofile(data, writter):
   for d in data:
      # print(d)
      snippet = d["snippet"]
      videoId = d["id"]["videoId"]
      date = snippet["publishedAt"]
      writter.writerow([snippet["title"], f"https://www.youtube.com/watch?v={videoId}", snippet["channelId"], date])
if __name__ == "__main__":
    main()