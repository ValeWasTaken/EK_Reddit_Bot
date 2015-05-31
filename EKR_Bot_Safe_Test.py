# EVE: Online Killmail Reddit Bot (EKRB) - Python 2.7
# ----------------------------------------------------
#                 SAFE TEST VERSION.
# ----------------------------------------------------
# This version does not interact with Reddit.
# Feel free to fork and modify this code to test changes.
#
# See How_to_contribute.md for more.

from bs4 import BeautifulSoup # Web scraping
import re       # Regex
import requests # Allows for catching ConnectionErrors and rerunning the program.
import time     # Timer for running the bot every set amount of time
import urllib	# Access internet and make network requests

def condense_value(num, suffix='ISK'):
    '''
        condense_vale() condenses the ISK (EVE-online currency) values from
        Examples such as: "123,456,789.00 ISK"
        Into neater forms such as: "123.46 million ISK"
    '''
    if num > 999999999999999:
        return("%s %s") % (num,suffix)
    else:
        for unit in ['','thousand','million','billion','trillion']:
            if abs(num) < 1000.0:
                return "%.2f %s %s" % (num, unit, suffix)
            num /= 1000.0

def startswith_vowel(string):
    return string.lower()[0] in 'aeiou'

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
            if startswith_vowel(v_ship_type):
                    v_ship_type = 'n ' + v_ship_type
            else:
                    v_ship_type = ' ' + v_ship_type
            v_rigging_text = soup.find_all('ul', class_="dropdown-menu")[3].find('a').get_text()
            v_rigging_link = soup.find_all('ul', class_="dropdown-menu")[3].find_all('a', href=re.compile('/o.smium.org/loadout/'))[0]['href']
            
            kb_ship_type = soup.find_all('tr', class_="attacker")[0].find_all('a', href=re.compile('/ship/'))[0].img.get('alt') #Ex: Nyx
            if startswith_vowel(kb_ship_type):
                    kb_ship_type = 'n ' + kb_ship_type
            else:
                    kb_ship_type = ' ' + kb_ship_type
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
                    reply_data.append("\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in system %s by %s of (%s | %s) flying a%s along with %s others."
                                      % (date, v_ship_type, v_pilot_name, v_corp, v_alliance, system, kb_pilot_name, kb_corp, kb_alliance, kb_ship_type, other_pilots))
            else:
                    kb_pilot_name = soup.find_all('td', style="text-align: center;")[0].find_all('a', href=re.compile('/character/'))[0].img.get('alt')
                    people_data = ("\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in system %s by %s flying a%s along with %s other"
                                   % (date, v_ship_type, v_pilot_name, v_corp, v_alliance, system, kb_pilot_name, kb_ship_type, other_pilots))
                    if int(other_pilots) == 1:
                            people_data += "."
                    else:
                            people_data += "s."
                    reply_data.append(people_data)
            reply_data.append("\n\n>Value dropped: %s\n\n>Value destroyed: %s\n\n>Total value: %s\n\n>[%s's %s](%s)\n\n"
                              % (isk_dropped, isk_destroyed, isk_total, v_pilot_name, v_rigging_text, v_rigging_link) + ('-'*50))
        reply_data = ('\n\n'.join(reply_data))
        
        msg_bot_link = 'http://www.reddit.com/message/compose?to=Killmail_Bot'
        github_link = 'https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot.py'
        
        print("Hi, I am a killmail reader bot. Let me summarize killmail for you!"
        + reply_data
        +"\n\n^^This ^^bot ^^is ^^open ^^source ^^& ^^in ^^active ^^development! ^^Please ^^feel ^^free ^^to ^^contribute: ^^[Suggestions](%s) ^^| ^^[Code](%s)") % (msg_bot_link, github_link)

# Edit line below to change or add killmails.
read_killmail(['https://zkillboard.com/kill/46955779/'])
