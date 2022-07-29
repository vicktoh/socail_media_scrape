import json
import csv


def parseFile(filename, topic):
   fhandle = open(f"{filename}.json", "r")
   file = open(f"general/youtube{topic}.csv", "w")
   writter = csv.writer(file)
   data= json.loads(fhandle.read())
   writter.writerow(["title", "link", "channelId", "date"])
   for d in data:
      # print(d)
      snippet = d["snippet"]
      videoId = d["id"]["videoId"]
      date = snippet["publishedAt"]
      writter.writerow([snippet["title"], f"https://www.youtube.com/watch?v={videoId}", snippet["channelId"], date])
   print("done")
parseFile("youtube-oby ezekwesili", "oby-ezkwesili")


   