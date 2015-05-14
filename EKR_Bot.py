# EVE: Online Killmail Reddit Bot (EKRB)

import urllib   # Access internet and make network requests
import re       # Regex
import praw     # Python Reddit API Wrapper
from bs4 import BeautifulSoup # Web scraping
import time     # Timer for running the bot every set amount of time
import requests # Allows for catching ConnectionErrors and rerunning the program.

r = praw.Reddit(user_agent='EVE: Online Killmail Reader Bot v1.945 - Created by /u/Valestrum '
                                'Designed to help users get killmail info without clicking links.')
r.login('UsernameHere','PasswordHere')
loop_count = 0

def condense_value(num, suffix='ISK'):
    if num > 999999999999999:
        return("%s %s") % (num,suffix)
    else:
        for unit in ['','thousand','million','billion','trillion']:
            if abs(num) < 1000.0:
                return "%.2f %s %s" % (num, unit, suffix)
            num /= 1000.0

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
                    if mail.startswith('https://zkill') or mail.startswith('http://zkill'):
                        mails.append(str(mail))
                existing.append(comment.id)
                cache.write(comment.id + '\n')
                print("I found a new comment! The ID is: " + comment.id)
                report = read_killmail(mails)
                comment.reply(report)

def read_killmail(killmails):
        reply_data = []
        for url in killmails:
            soup = BeautifulSoup(urllib.urlopen(url).read())
            isk_dropped = soup.find("td", class_="item_dropped").get_text()
            isk_destroyed = soup.find("td", class_="item_destroyed").get_text()
            isk_total = soup.find("strong", class_="item_dropped").get_text()
            isk_dropped, isk_destroyed, isk_total = [condense_value(int(value[:-7].replace(',',''))) for value in [isk_dropped, isk_destroyed, isk_total]]

            system = soup.find_all('a', href=re.compile('/system/'))[1].get_text() #Ex: Iralaja
            date = soup.find("table", class_="table table-condensed table-striped table-hover").find_all('td')[3].get_text()[:10]
            if len(date) < 6:
                    date = soup.find("table", class_="table table-condensed table-striped table-hover").find_all('td')[2].get_text()[:10]
            other_pilots = int(str(soup.find("th", class_="hidden-md hidden-xs").get_text())[:-9])-1 #Ex: '44' out of "45 Involved", excluded 1 being kb
            
            #v = victim, kb = pilot firing killing blow
            v_pilot_info = soup.find("table", class_="table table-condensed").find_all('td')[2].get_text().split('\n\n')
            v_pilot_name = v_pilot_info[0]
            if len(v_pilot_info) > 1:
                    v_corp = v_pilot_info[1]
                    if len(v_pilot_info) > 3: # This accounts for extra variable '' added to v_pilot_info
                            v_alliance = v_pilot_info[2]
                    else:
                            v_alliance = '<No Alliance>'
            else:
                    v_corp = '<No Corp>'
                    v_alliance = '<No Alliance>'
                    
            v_ship_type = (''.join(((soup.find("td", style="width: 100%").get_text())).split())) # Ex: Leviathan(Titan)
            if v_ship_type[0].lower() in 'aeiou':
                    v_ship_type = 'n '+str(v_ship_type)
            else:
                    v_ship_type = ' '+str(v_ship_type)
            v_rigging_text = soup.find_all('ul', class_="dropdown-menu")[3].find('a').get_text()
            v_rigging_link = soup.find_all('ul', class_="dropdown-menu")[3].find_all('a', href=re.compile('/o.smium.org/loadout/'))[0]['href']
            
            kb_ship_type = soup.find_all('tr', class_="attacker")[0].find_all('a', href=re.compile('/ship/'))[0].img.get('alt') #Ex: Nyx
            if kb_ship_type[0].lower() in 'aeiou':
                    kb_ship_type = 'n '+str(kb_ship_type)
            else:
                    kb_ship_type = ' '+str(kb_ship_type)
            if int(other_pilots) == 0:
                    kb_pilot_info = soup.find('div', class_="hidden-sm hidden-md hidden-xs").get_text().split('\n\n')
                    kb_pilot_name = kb_pilot_info[0]
                    if len(kb_pilot_info) > 1:
                            kb_corp = kb_pilot_info[1]
                            if len(kb_pilot_info) > 3:
                                    kb_alliance = kb_pilot_info[2]
                            else:
                                    kb_alliance = '<No Alliance>'
                    else:
                            kb_corp = '<No Corp>'
                            kb_alliance = '<No Alliance>'
                    reply_data.append("\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in system %s by %s of (%s | %s) flying a%s along with %s others." % (date,v_ship_type,v_pilot_name,v_corp,v_alliance,system,kb_pilot_name,kb_corp,kb_alliance,kb_ship_type,other_pilots))
            else:
                    kb_pilot_name = soup.find_all('td', style="text-align: center;")[0].find_all('a', href=re.compile('/character/'))[0].img.get('alt')
                    if int(other_pilots) == 1:
                            reply_data.append("\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in system %s by %s flying a%s along with %s other." % (date,v_ship_type,v_pilot_name,v_corp,v_alliance,system,kb_pilot_name,kb_ship_type,other_pilots))
                    else:
                            reply_data.append("\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in system %s by %s flying a%s along with %s others." % (date,v_ship_type,v_pilot_name,v_corp,v_alliance,system,kb_pilot_name,kb_ship_type,other_pilots))
            reply_data.append("\n\n>Value dropped: %s\n\n>Value destroyed: %s\n\n>Total value: %s\n\n>[%s's %s](%s)\n\n" % (isk_dropped,isk_destroyed,isk_total,v_pilot_name,v_rigging_text,v_rigging_link)+('-'*50))
        reply_data = ('\n\n'.join(reply_data))

        return("Hi, I am a killmail reader bot. Let me summarize killmail for you!"
        +str(reply_data)
        +"\n\n^^This ^^bot ^^is ^^open ^^source ^^& ^^in ^^active ^^development! ^^Please ^^feel ^^free ^^to ^^contribute: ^^[Suggestions](%s) ^^| ^^[Code](%s)") % ('http://www.reddit.com/message/compose?to=Killmail_Bot','https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot.py')

while True:
    try:
        run_bot()
    except requests.ConnectionError as e:
        print e
        time.sleep(60)
        run_bot()
    loop_count += 1
    print("Program loop #"+str(loop_count)+" completed successfully.")
    time.sleep(1200)
