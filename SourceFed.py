import json
import requests
import praw
from random import shuffle
import os
from time import sleep
from config_bot import *
r=praw.Reddit(client_id=rid,client_secret=rsecret,user_agent=ua,password=REDDIT_PASS,username=REDDIT_USERNAME)
#print(r.user.me())
pageToken="CDIQAQ"
req=requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&pageToken="+pageToken+"&playlistId=PL0ufum6QEeRyMfja25IqrEX84Pzdp4sgb&key="+key)
data=json.loads(req.text)
vids=[]
numVids=data["pageInfo"]["totalResults"]
print(numVids)
perPage=data["pageInfo"]["resultsPerPage"]
num=0
sub=r.subreddit("SourceFed")
while True:
    try:
        if not os.path.isfile("posted.txt"):
            posted=[]
        else:
            broke=False
            with open("posted.txt","r") as f:
                posted=f.read()
                posted=posted.split("\n")
            if numVids!=data["pageInfo"]["totalResults"]:
                numVids=data["pageInfo"]["totalResults"]
                print(numVids)
                num=0
            while num<numVids:
                req=requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&pageToken="+pageToken+"&playlistId=PL0ufum6QEeRyMfja25IqrEX84Pzdp4sgb&key="+key)
                data=json.loads(req.text)
                if "nextPageToken" in data:
                    pageToken=data["nextPageToken"]
                vids=data["items"]+vids
                num+=perPage
            shuffle(vids)
            for vid in vids:
                videoId=vid["contentDetails"]["videoId"]
                if videoId not in posted:
                    title="SourceFed Memories: "+vid["snippet"]["title"]
                    post=sub.submit(title,url="http://youtube.com/watch?v="+videoId)
                    print("Posted "+title)
                    post.reply("This submission was automatically submitted by a bot.\n\n[Author](/u/friedkeenan)\n\n[Relevant Link](https://www.reddit.com/r/SourceFed/comments/61754u/in_light_of_sourcefed_being_cancelled_ive_made/)\n\n[Source Code](http://github.com/friedkeenan/Sourcefed)")
                    posted.append(videoId)
                    broke=True
                    break
            if not broke:
                r.redditor("friedkeenan").message("Out of videos","Start me up again?")
            sleep(24*60*60)
        with open("posted.txt","w") as f:
            for videoId in posted:
                f.write(videoId+"\n")
    except:
        r=praw.Reddit(client_id=rid,client_secret=rsecret,user_agent=ua,password=REDDIT_PASS,username=REDDIT_USERNAME)
        print("Had to re-praw. If that's not true then poo")
