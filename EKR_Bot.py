# EVE: Online Killmail Reddit Bot (EKRB)

import urllib   # Access internet and make network requests
import re       # Regex
import praw     # Python Reddit API Wrapper
from bs4 import BeautifulSoup # Web scraping
import time

r = praw.Reddit(user_agent='EVE: Online Killmail Reader Bot v1.6 - Created by /u/Valestrum '
                                'Designed to help users get killmail info without clicking links.')
r.login('UsernameHere','PasswordHere')
loopCount = 0

def run_bot():
    with open('cache.txt','r') as cache:
        existing = cache.read().splitlines()

    subreddit = r.get_subreddit("eve")
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
            
            #v = victim, kb = pilot firing killing blow
            vPilotName = soup.table.table.tr.a.get('title')
            vShipType = (''.join(((soup.find("td", style="width: 100%").get_text())).split())) # Ex: Leviathan(Titan)
            vRiggingText = soup.find_all('ul', class_="dropdown-menu")[3].find('a').get_text()
            vRiggingLink = soup.find_all('ul', class_="dropdown-menu")[3].find_all('a', href=re.compile('/o.smium.org/loadout/'))[0]['href']
            #Add v corp and alliance here
            kbShipType = soup.find_all('tr', class_="attacker")[0].find_all('a', href=re.compile('/ship/'))[0].img.get('alt') #Ex: Nyx
            kbPilotName = soup.find_all('td', style="text-align: center;")[0].find_all('a', href=re.compile('/character/'))[0].img.get('alt')
            #Add kb corp and alliance here
            system = soup.find_all('a', href=re.compile('/system/'))[0].get_text() #Ex: Iralaja
            otherPilots = int(str(soup.find("th", class_="hidden-md hidden-xs").get_text())[:-9])-1 #Ex: '44' out of "45 Involved", excluded 1 being kb
            
            replyData.append("\n\n>A %s piloted by %s was destroyed in system %s by %s flying a %s along with %s others." % (vShipType,vPilotName,system,kbPilotName,kbShipType,otherPilots)
                    +"\n\n>Value dropped: %s\n\n>Value destroyed: %s\n\n>Total value: %s\n\n>[%s](%s)\n\n" % (iskDropped,iskDestroyed,iskTotal,vRiggingText,vRiggingLink)+('-'*50))
        replyData = ('\n\n'.join(replyData))

        return("Hi, I am a killmail reader bot. Let me summarize killmail for you!"
        +str(replyData)
        +"\n\n^^This ^^bot ^^is ^^open ^^source ^^and ^^in ^^development! ^^Please ^^feel ^^free ^^to ^^contribute ^^[here](https://github.com/ArnoldM904/EK_Reddit_Bot) ^^and/or ^^PM ^^with ^^suggestions!")

while True:
    run_bot()
    loopCount += 1
    print("Program loop #"+str(loopCount)+" completed successfully.")
    time.sleep(1200)
