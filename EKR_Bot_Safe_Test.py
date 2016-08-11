# EVE: Online Killmail Reddit Bot (EKRB) - Python 2.7
# ----------------------------------------------------
#                 SAFE TEST VERSION.
# ----------------------------------------------------
# This version does not interact with Reddit.
# Feel free to fork and modify this code to test changes.
#
# See How_to_contribute.md for more.

from bs4 import BeautifulSoup   # Web scraping
import re                       # Regex
import requests                 # ConnectionErrors, rerunning the program.
import urllib   # Access internet and make network requests


startswith_vowel = lambda string: string.lower()[0] in 'aeiou'


def condense_value(num, suffix='ISK'):
    '''
        condense_value() condenses the ISK (EVE-online currency) values from
        Examples such as: "123,456,789.00 ISK"
        Into neater forms such as: "123.46 million ISK"
    '''
    if num > 999999999999999:
        return("%s %s") % (num, suffix)
    else:
        for unit in ['', 'thousand', 'million', 'billion', 'trillion']:
            if abs(num) < 1000.0:
                return "%.2f %s %s" % (num, unit, suffix)
            num /= 1000.0
            

def read_killmail(killmails):
    ''' 
        read_killmail() consists of 4 main parts that serve to scrape
        zkillboard.com and then return the information in a way that is
        suited for a Reddit comment.

        Part 1 - Cycle through the killmail(s)
        Part 2 - Scrape the "TL;DR" of their information
        Part 3 - Append it all into a string using Reddit-friendly syntax
        Part 4 - Return the correctly formatted string with scraped
                 information to be used in the reply comment.
    '''
    reply_data = []
    # Part 1
    for url in killmails:
        # Part 2
        soup = BeautifulSoup(urllib.urlopen(url).read(), "html.parser")
        isk_dropped = soup.find("td", class_="item_dropped").get_text()
        isk_destroyed = soup.find("td", class_="item_destroyed").get_text()
        isk_total = soup.find("strong", class_="item_dropped").get_text()
        isk_dropped, isk_destroyed, isk_total = [
            condense_value(int(value[:-7].replace(',', ''))) for
            value in [isk_dropped, isk_destroyed, isk_total]
            ]

        system = soup.find_all('a', href=re.compile('/system/'))
        system = system[1].get_text()  # Ex: Iralaja
        date = soup.find('td', class_="info_kill_dttm").get_text()[:10]

        # Ex: '44' out of "45 Involved", excluded 1 being kb
        pilot_class = "hidden-md hidden-xs"
        other_pilots = int(str(
            soup.find("th", class_=pilot_class).get_text())[:-9])-1

        # v = victim, kb = pilot firing killing blow
        info_class = "table table-condensed"
        v_pilot_info = soup.find("table", class_=info_class)
        v_pilot_info = v_pilot_info.find_all('td')[2].get_text().split('\n\n')
        v_pilot_name = v_pilot_info[0]
        if len(v_pilot_info) > 1:
            v_corp = v_pilot_info[1]
            # This accounts for extra variable '' added to v_pilot_info
            if len(v_pilot_info) > 3:
                v_alliance = v_pilot_info[2]
            else:
                v_alliance = '<No Alliance>'
        else:
            v_corp = '<No Corp>'
            v_alliance = '<No Alliance>'

        v_ship_type = ''.join(
            (soup.find("td", style="width: 100%").get_text()).split()
            ) # Ex: Leviathan(Titan)
        if startswith_vowel(v_ship_type):
            v_ship_type = 'n ' + v_ship_type
        else:
            v_ship_type = ' ' + v_ship_type
        v_rigging_text = soup.find_all('ul', class_="dropdown-menu")[3]
        v_rigging_text = v_rigging_text.find('a').get_text()
        v_rigging_link = soup.find_all('ul', class_="dropdown-menu")[3]
        v_rigging_link = v_rigging_link.find_all(
            'a', href=re.compile('/o.smium.org/loadout/'))[0]['href']

        kb_ship_type = soup.find_all('tr', class_="attacker")[0]
        kb_ship_type = kb_ship_type.find_all(
            'a', href=re.compile('/ship/'))[0].img.get('alt') # Ex: Nyx
        if startswith_vowel(kb_ship_type):
            kb_ship_type = 'n ' + kb_ship_type
        else:
            kb_ship_type = ' ' + kb_ship_type
        if int(other_pilots) == 0:
            p_info_class = "hidden-sm hidden-md hidden-xs"
            kb_pilot_info = soup.find('div', class_=p_info_class)
            kb_pilot_info = kb_pilot_info.get_text().split('\n\n')
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
            # Part 3
            reply_data.append(
                "\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed "
                "in system %s by %s of (%s | %s) flying a%s along with %s"
                "others." % (
                    date, v_ship_type, v_pilot_name, v_corp,
                    v_alliance, system, kb_pilot_name, kb_corp,
                    kb_alliance, kb_ship_type, other_pilots))
        else:
            kb_pilot_name = soup.find_all('td', style="text-align: center;")[0]
            kb_pilot_name = kb_pilot_name.find_all(
                'a', href=re.compile('/character/'))[0].img.get('alt')
            people_data = (
                "\n\n>On %s a%s piloted by %s of (%s | %s) was destroyed in "
                "system %s by %s flying a%s along with %s other" % (
                    date, v_ship_type, v_pilot_name, v_corp,
                    v_alliance, system, kb_pilot_name,
                    kb_ship_type, other_pilots))
            if int(other_pilots) == 1:
                people_data += "."
            else:
                people_data += "s."
            reply_data.append(people_data)
        reply_data.append(
            "\n\n>Value dropped: %s\n\n>Value destroyed: %s\n\n>Total value: "
            "%s\n\n>[%s's %s](%s)\n\n" % (
                isk_dropped, isk_destroyed, isk_total,
                v_pilot_name, v_rigging_text, v_rigging_link)
                + ('-'*50))
    reply_data = ('\n\n'.join(reply_data))

    # Part 4
    msg_bot_link = 'http://www.reddit.com/message/compose?to=Killmail_Bot'
    github_link = 'https://github.com/ArnoldM904/' \
                  'EK_Reddit_Bot/blob/master/EKR_Bot.py'

    print(
        "Hi, I am a killmail reader bot. "
        "Let me summarize that for you!" +
        reply_data +
        "\n\n^^This ^^bot ^^is ^^open ^^source ^^& ^^in ^^active "
        "^^development! ^^Please ^^feel ^^free ^^to ^^contribute: ^^["
        "Suggestions](%s) ^^| ^^[Code](%s)") % (
            msg_bot_link, github_link)


# Edit line below to change or add killmails.
read_killmail(['https://zkillboard.com/kill/46955779/'])
# Note: You can check multiple killmails at once like so.. 
read_killmail(['https://zkillboard.com/kill/49975474/','https://zkillboard.com/kill/49860622/','https://zkillboard.com/kill/49861044/'])
