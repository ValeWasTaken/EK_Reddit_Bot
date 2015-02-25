# EVE: Online Killmail Reddit Bot (EKRB)

import urllib   # Access internet and make network requests
import re       # Regex
import praw     # Python Reddit API Wrapper
import time

r = praw.Reddit(user_agent='EVE: Online Killmail Reader Bot v1.1 - Created by /u/Valestrum '
                                'Designed to help users get killmail info without clicking links.')
r.login('UsernameHere','PasswordHere')
loopCount = 0

def run_bot():
    with open('cache.txt','r') as cache:
        existing = cache.read().splitlines()

    subreddit = r.get_subreddit("eve")
    comments = subreddit.get_comments(limit=100)

    with open('cache.txt', 'a+') as cache:
        for comment in comments:
            comment_text = comment.body.lower()

            #Records any relevant URLs.
            killmail = [item for item in comment_text.split() if re.match(r"https://zkillboard\.com/kill/*", item)]

            if killmail and comment.id not in existing: #if killmail list is not empty and bot has never messaged
                killmail = killmail[0]
                if killmail[:13] == 'https://zkill' or killmail[:12] == 'http://zkill':
                    existing.append(comment.id)
                    cache.write(comment.id + '\n')
                    print("I found a new comment! The ID is: " + comment.id)
                    report = read_killmail(killmail)
                    comment.reply(report)

def read_killmail(killmail):
        url = [killmail]
        i = 0
        iskDroppedSource = '<td class="item_dropped">(.+?)</td>' # Gets whatever is inbetween the tags
        iskDestroyedSource = '<td class="item_destroyed">(.+?)</td>'
        iskTotalSource = '<strong class="item_dropped">(.+?)</strong>'

        iskDroppedText = re.compile(iskDroppedSource) # Converts regex string into something that can be interpreted by regular library
        iskDestroyedText = re.compile(iskDestroyedSource)
        iskTotalText = re.compile(iskTotalSource)

        html = urllib.urlopen(url[i]).read()

        iskDropped = re.findall(iskDroppedText,html)
        iskDestroyed = re.findall(iskDestroyedText,html)
        iskTotal = re.findall(iskTotalText,html)

        return("Hi, I am a killmail reader bot. Let me summarize this killmail for you!"
        +"\n\n>Value dropped: " + str(iskDropped[0])
        +"\n\n>Value destroyed: " + str(iskDestroyed[0])
        +"\n\n>Total value: " + str(iskTotal[0])
        +"\n\n^^This ^^bot ^^is ^^brand ^^new ^^please ^^be ^^gentle. ^^Please ^^PM ^^with ^^suggestions!")

while True:
    run_bot()
    loopCount += 1
    print("Program loop #"+str(loopCount)+" completed successfully.")
    time.sleep(1200)
