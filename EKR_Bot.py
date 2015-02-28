# EVE: Online Killmail Reddit Bot (EKRB)

import urllib   # Access internet and make network requests
import re       # Regex
import praw     # Python Reddit API Wrapper
from bs4 import BeautifulSoup # Web scraping
import time

r = praw.Reddit(user_agent='EVE: Online Killmail Reader Bot v1.1 - Created by /u/Valestrum '
                                'Designed to help users get killmail info without clicking links.')
r.login('UsernameHere','PasswordHere')
loopCount = 0

def run_bot():
    with open('cache.txt','r') as cache:
        existing = cache.read().splitlines()

    subreddit = r.get_subreddit("test")
    comments = subreddit.get_comments(limit=150)

    with open('cache.txt', 'a+') as cache:
        for comment in comments:
            comment_text = comment.body.lower()

            #Records any relevant URLs.
            killmails = [item for item in comment_text.split() if re.match(r"https://zkillboard\.com/kill/*", item)]

            if killmails and comment.id not in existing: #if killmail list is not empty and bot has never messaged
                mails = []
                for mail in killmails:
                    if mail[:13] == 'https://zkill' or mail[:12] == 'http://zkill':
                        mails.append(str(mail))
                existing.append(comment.id)
                cache.write(comment.id + '\n')
                print("I found a new comment! The ID is: " + comment.id)
                report = read_killmail(mails)
                comment.reply(report)

def read_killmail(killmails):
        replyData = []
        for url in killmails:
            soup = BeautifulSoup(urllib.urlopen(url).read())
            iskDropped = soup.find("td", class_="item_dropped").get_text()
            iskDestroyed = soup.find("td", class_="item_destroyed").get_text()
            iskTotal = soup.find("strong", class_="item_dropped").get_text()
            replyData.append("\n\n>Value dropped: " + str(iskDropped) +"\n\n>Value destroyed: " + str(iskDestroyed) +"\n\n>Total value: " + str(iskTotal)+'\n\n'+('-'*20))
        replyData = ('\n\n'.join(replyData))

        return("Hi, I am a killmail reader bot. Let me summarize killmail for you!"
        +str(replyData)
        +"\n\n^^This ^^bot ^^is ^^brand ^^new ^^please ^^be ^^gentle. ^^Please ^^PM ^^with ^^suggestions!")

while True:
    run_bot()
    loopCount += 1
    print("Program loop #"+str(loopCount)+" completed successfully.")
    time.sleep(1200)
