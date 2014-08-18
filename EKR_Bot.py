# !! Note: !! This program currently does not have Reddit interaction enabled. 
# This is only the web-scraped information half.

# EVE: Online Killmail Reddit Bot (EKRB)
# Created by: Reddit.com/u/Valestrum

import urllib   # Access internet and make network requests
import re       # Regex
import praw     # Python Reddit API Wrapper

r = praw.Reddit(user_agent='EVE: Online Killmail Reader Bot v1.0 - Created by /u/Valestrum '
                                'https://github.com/ArnoldM904/EK_Reddit_Bot')
r.login('InsertUsernameHere','InsertPasswordHere')

# -- Insert large work-in-progress code that I'm too ashamed to show here. -- 

def readKillmail():
        killmail = "https://zkillboard.com/kill/38412453/" # Change this to be user's killmail.
        url = [killmail]
        i = 0
        iskDroppedSource = '<td class="item_dropped">(.+?)</td>' # Gets whatever is inbetween the tags
        iskDestroyedSource = '<td class="item_destroyed">(.+?)</td>'
        iskTotalSource = '<strong class="item_dropped">(.+?)</strong>'

        iskDroppedText = re.compile(iskDroppedSource) # Converts above regex string into something that can be interpreted by regular library
        iskDestroyedText = re.compile(iskDestroyedSource)
        iskTotalText = re.compile(iskTotalSource)

        html = urllib.urlopen(url[i]).read()

        iskDropped = re.findall(iskDroppedText,html)
        iskDestroyed = re.findall(iskDestroyedText,html)
        iskTotal = re.findall(iskTotalText,html)

        print("Hi, I am a killmail reader bot. Let me summarize this killmail for you!")
        print("Value dropped: " + str(iskDropped[0]))
        print("Value destroyed: " + str(iskDestroyed[0]))
        print("Total value: " + str(iskTotal[0]))
        print("^^This ^^bot ^^is ^^brand ^^new ^^please ^^be ^^gentle. ^^PM ^^for ^^questions.")
