import snscrape.modules.twitter as sntwitter
import snscrape.modules.instagram as sninsta
import threading
import sys
import csv

# influencer = sys.argv[1]

influencers = ["dabiodunMFR", "mrmacaronii", "RealSeunKuti", "AishaYesufu", "AreaFada1",
               ]
topics = ["Ethnicity", "corruption", "Nigeria is not working", "constitution", "constitutionalism", "1999 constitution", "Nigerian constitution", "rule of law", "justice", "exclusive list", "concurrent list", "separation of power", "peace", "security", "law and order", "insecurity", "insurgency", "security votes"]
header = ["username", "displayName", "tweet",
          "likes", "retweets", "link", "date"]
instagram=["username", "url", "content", "likes", "comment", "video", "date"]
instagram_hashtags = ["endsars","fulani", "herdsmen" "kidnapping", "muslim", "nothern nigeria", "ipob", "bokoharam", "governance", "terrorism nigeria", "niger delta", "national assembly", "power", "bandits", "insurgency"]

def format_user_search():
   influcencernames = [f'from:{influencer}' for influencer in influencers]
   return " OR ".join(influcencernames)

def scrape_insta(topic):
   file = open(f"new/instagram/{topic}.csv", "w")
   writter = csv.writer(file)
   writter.writerow(instagram)
   limit = 50000
   run = 0
   for post in sninsta.InstagramHashtagScraper(topic).get_items():
      writter.writerow([post.username, post.url, post.content, post.likes, post.comments, post.isVideo, post.date])
      run+=1
      if(run >= limit):
         break
   file.close()
   print(f'finished scrapinging #{topic}')

def scrapetweets(query, topic):
   #change to disired folder
   output_dir = "new/twitter/"
   file = open(f'{output_dir}{topic}.csv', "w")
   writter = csv.writer(file)
   writter.writerow(header)
   limit = 50000
   run=0
   print(f'running thread for {topic}')
   for tweet in sntwitter.TwitterSearchScraper(query).get_items():
      writter.writerow([tweet.user.username, tweet.user.displayname, tweet.content,
                       tweet.likeCount, tweet.retweetCount, tweet.url, tweet.date])
      run += 1
      if run >= limit:
         break
   print(f'Finished {topic} for')
   file.close()

# scrapetweets("from:AishaYesufu", "AishaYesufu")
def scrapeThreadhing():
   ts = []
   users_query_chunk = format_user_search()
   for topic in topics:
      query = f'{topic} since:2020-01-01'
      t = threading.Thread(target=scrape_insta, args=(topic,))
      t.start()
      ts.append(t)
   print("Waiting for threads to end")
   for t in ts:
      t.join()
scrapeThreadhing()

# Instagram scrape
# ts = []
# users_query_chunk = format_user_search()
# for topic in instagram_hashtags:
#    t = threading.Thread(target=scrape_insta, args=(topic,))
#    t.start()
#    ts.append(t)
# print("Waiting for threads to end")
# for t in ts:
#    t.join()
