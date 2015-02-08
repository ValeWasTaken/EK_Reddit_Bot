# !! Note: !! This program currently not finished. Please check back soon to see updates!

# EVE: Online Killmail Reddit Bot (EKRB)

import urllib   # Access internet and make network requests
import re       # Regex
import praw     # Python Reddit API Wrapper

r = praw.Reddit(user_agent='EVE: Online Killmail Reader Bot v0.5 - Created by /u/Valestrum '
                                'Designed to help users get killmail info without clicking links.')
r.login('InsertUsernameHere','InsertPasswordHere')

def run_bot():
    with open('cache.txt','r') as cache:
        existing = cache.read().splitlines()

    subreddit = r.get_subreddit("test") # For testing only. Will eventually go to EVE subreddits.
    print("Grabbing comments..") # For testing only to see where the program is at.
    comments = subreddit.get_comments(limit=10)

    with open('cache.txt', 'a+') as cache:
        for comment in comments:
            comment_text = comment.body.lower()
            
            #Defines the check to see if the comment meets the criteria the bot is looking for.
            #isMarch = (comment contains killmail link)
            killmail = 'https://zkillboard.com/kill/38412453/' # Replace with user's link

            #Check that comment hasn't been seen before and that it meets the desired critera.
            if comment.id not in existing and isMatch:
                    existing.append(comment.id)
                    cache.write(comment.id + '\n')
                    report = read_killmail(killmail)
                    comment.reply(report)
                    print("I found a new comment! The ID is: " + comment.id)
            
    print("Comment loop finished.")  # For testing only to see where the program is at.

def read_killmail(killmail):
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

        return("Hi, I am a killmail reader bot. Let me summarize this killmail for you!"
        +"\n*Value dropped: *" + str(iskDropped[0])
        +"\n*Value destroyed: *" + str(iskDestroyed[0])
        +"\n*Total value: *" + str(iskTotal[0])
        +"\n^^This ^^bot ^^is ^^brand ^^new ^^please ^^be ^^gentle. ^^PM ^^for ^^questions.")

while True:
    run_bot()
    time.sleep(60)   
