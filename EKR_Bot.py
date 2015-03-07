# EVE: Online Killmail Reddit Bot (EKRB)

import urllib   # Access internet and make network requests
import re       # Regex
import praw     # Python Reddit API Wrapper
from bs4 import BeautifulSoup # Web scraping
import time

r = praw.Reddit(user_agent='EVE: Online Killmail Reader Bot v1.92 - Created by /u/Valestrum '
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

            dropRounded = (int((iskDropped)[:-7].replace(',','')) / 1000000.0)
            destroyedRounded = (int((iskDestroyed)[:-7].replace(',','')) / 1000000.0)
            totalRounded = (int((iskTotal)[:-7].replace(',','')) / 1000000.0)
            
            if dropRounded > 1000:
                    dropRounded /= 1000
                    iskDropped = ('%.2f billion ISK') % dropRounded
            else:
                    iskDropped = ('%.2f million ISK') % dropRounded
            if destroyedRounded > 1000:
                    destroyedRounded /= 1000
                    iskDestroyed = ('%.2f billion ISK') % destroyedRounded
            else:
                    iskDestroyed = ('%.2f million ISK') % destroyedRounded
            if totalRounded > 1000:
                    totalRounded /= 1000
                    iskTotal = ('%.2f billion ISK') % totalRounded
            else:
                    iskTotal = ('%.2f million ISK') % totalRounded

            system = soup.find_all('a', href=re.compile('/system/'))[0].get_text() #Ex: Iralaja
            date = soup.find("table", class_="table table-condensed table-striped table-hover").find_all('td')[3].get_text()[:10]
            if len(date) < 6:
                    date = soup.find("table", class_="table table-condensed table-striped table-hover").find_all('td')[2].get_text()[:10]
            otherPilots = int(str(soup.find("th", class_="hidden-md hidden-xs").get_text())[:-9])-1 #Ex: '44' out of "45 Involved", excluded 1 being kb
            
            #v = victim, kb = pilot firing killing blow
            vPilotInfo = soup.find("table", class_="table table-condensed").find_all('td')[2].get_text().split('\n\n')
            vPilotName = vPilotInfo[0]
            if len(vPilotInfo) > 1:
                    vCorp = vPilotInfo[1]
                    if len(vPilotInfo) > 3: # This accounts for extra variable '' added to PilotInfo
                            vAlliance = vPilotInfo[2]
                    else:
                            vAlliance = '<No Alliance>'
            else:
                    vCorp = '<No Corp>'
                    vAlliance = '<No Alliance>'
                    
            vShipType = (''.join(((soup.find("td", style="width: 100%").get_text())).split())) # Ex: Leviathan(Titan)
            if vShipType[0].lower() in 'aeiou':
                    vShipType = 'n '+str(vShipType)
            else:
                    vShipType = ' '+str(vShipType)
            vRiggingText = soup.find_all('ul', class_="dropdown-menu")[3].find('a').get_text()
            vRiggingLink = soup.find_all('ul', class_="dropdown-menu")[3].find_all('a', href=re.compile('/o.smium.org/loadout/'))[0]['href']
            
            kbShipType = soup.find_all('tr', class_="attacker")[0].find_all('a', href=re.compile('/ship/'))[0].img.get('alt') #Ex: Nyx
            if kbShipType[0].lower() in 'aeiou':
                    kbShipType = 'n '+str(kbShipType)
            else:
                    kbShipType = ' '+str(kbShipType)
            if int(otherPilots) == 0:
                    kbPilotInfo = soup.find('div', class_="hidden-sm hidden-md hidden-xs").get_text().split('\n\n')
                    kbPilotName = kbPilotInfo[0]
                    if len(kbPilotInfo) > 1:
                            kbCorp = kbPilotInfo[1]
                            if len(kbPilotInfo) > 3:
                                    kbAlliance = kbPilotInfo[2]
                            else:
                                    kbAlliance = '<No Alliance>'
                    else:
                            kbCorp = '<No Corp>'
                            kbAlliance = '<No Alliance>'
                    replyData.append("\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in system %s by %s of (%s | %s) flying a%s along with %s others." % (date,vShipType,vPilotName,vCorp,vAlliance,system,kbPilotName,kbCorp,kbAlliance,kbShipType,otherPilots)
                    +"\n\n>Value dropped: %s\n\n>Value destroyed: %s\n\n>Total value: %s\n\n>[%s's %s](%s)\n\n" % (iskDropped,iskDestroyed,iskTotal,vPilotName,vRiggingText,vRiggingLink)+('-'*50))
            else:
                    kbPilotName = soup.find_all('td', style="text-align: center;")[0].find_all('a', href=re.compile('/character/'))[0].img.get('alt')
                    if int(otherPilots) == 1:
                            replyData.append("\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in system %s by %s flying a%s along with %s other." % (date,vShipType,vPilotName,vCorp,vAlliance,system,kbPilotName,kbShipType,otherPilots))
                    else:
                            replyData.append("\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in system %s by %s flying a%s along with %s others." % (date,vShipType,vPilotName,vCorp,vAlliance,system,kbPilotName,kbShipType,otherPilots)
                    +"\n\n>Value dropped: %s\n\n>Value destroyed: %s\n\n>Total value: %s\n\n>[%s's %s](%s)\n\n" % (iskDropped,iskDestroyed,iskTotal,vPilotName,vRiggingText,vRiggingLink)+('-'*50))
        replyData = ('\n\n'.join(replyData))

        return("Hi, I am a killmail reader bot. Let me summarize killmail for you!"
        +str(replyData)
        +"\n\n^^This ^^bot ^^is ^^open ^^source ^^& ^^in ^^active ^^development! ^^Please ^^feel ^^free ^^to ^^contribute: ^^[Suggestions](%s) ^^| ^^[Code](%s) ^^| ^^[ISK](%s)") % ('http://www.reddit.com/message/compose?to=Killmail_Bot','https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot.py','http://evewho.com/pilot/Valestrum+Vos')

while True:
    run_bot()
    loopCount += 1
    print("Program loop #"+str(loopCount)+" completed successfully.")
    time.sleep(1200)
