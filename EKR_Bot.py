# EVE: Online Killmail Reddit Bot (EKRB) - Version 2.0.45 - Python 2.7

from bs4 import BeautifulSoup   # Web scraping
import praw                     # Python Reddit API Wrapper
import re                       # Regex
import requests                 # ConnectionErrors, rerunning the program.
import time     # Timer for running the bot every set amount of time
import urllib   # Access internet and make network requests

r = praw.Reddit(
    user_agent='EVE: Online Killmail Reader v2.0.45'
               'Created by /u/Valestrum '
               'Designed to help users get killmail info without clicking '
               'links and to post threads on kills detected to be worth '
               '20 billion or more ISK.')
username, password = [line.rstrip('\n') for line in open('user_info.txt')]
r.login(username, password)
subreddit = r.get_subreddit("eve")
loop_count = 0
startswith_vowel = lambda string: string.lower()[0] in 'aeiou'


def find_kills():
    '''
        -- Exclusively used by thread posting portion of bot. -- 
        Check for 1 billion+ ISK value kills on zkillboard.com
        Then return the kill # to be used in check_cache()
    '''
    url = 'https://zkillboard.com/kills/10b/'
    soup = BeautifulSoup(urllib.urlopen(url).read(), "html.parser")

    kill_ids = []
    num_of_killmails = len(soup.find_all('a', href=re.compile('/kill/')))

    for x in range(num_of_killmails):
        # Only use every 3rd killmail due to each link being stated 3 times.
        if x % 3 == 0:
            kill_id = soup.find_all('a', 
                        href=re.compile('/kill/'))[x]['href'][:-9]
            kill_ids.append(kill_id)
    return(kill_ids)


def check_cache(kill_ids):
    '''
        -- Exclusively used by thread posting portion of bot. -- 
        Compare web-scraped kill_ids with ids already saved in cache.
        Then return the new ids found for analyze_kills()
    '''
    new_ids = []
    with open('recorded_kills.txt', 'r') as cache:
        existing = cache.read().splitlines()
    with open('recorded_kills.txt', 'a+') as cache:
        for kill_id in kill_ids:
            if kill_id not in(existing):
                existing.append(kill_id)
                new_ids.append(kill_id)
    return(new_ids)


def analyze_kills(new_ids):
    '''
        -- Exclusively used by thread posting portion of bot. -- 
        Analyze new kills found and record relevant information.
        Then return information for usage in post_threads()
    '''
    thread_info = []
    for new_id in new_ids:
        url = 'https://zkillboard.com' + new_id
        soup = BeautifulSoup(urllib.urlopen(url).read(), "html.parser")
    
        isk_worth = soup.find("strong", class_="item_dropped").get_text()
        isk_worth = condense_value(int(isk_worth[:-7].replace(',', '')))

        # Only record kills that are worth 20bil ISK or more.
        if float(isk_worth[:-5]) > 19.99:
            with open('recorded_kills.txt', 'a+') as cache:
                print("New 20b+ kill found! Kill #: " + new_id)
                cache.write(new_id + '\n')
            #time = soup.find('td', class_="info_kill_dttm").get_text()[11:]
            
            # v = victim
            v_pilot = soup.find_all(
                'a', href=re.compile('/character/'))[1].get_text()
            v_ship = soup.find_all(
                'a', href=re.compile('/ship/'))[1].get_text()
            try:
                v_corp = soup.find_all(
                    'a', href=re.compile('/corporation/'))[1].get_text()
            except IndexError:
                v_corp = "<No Corp>"
            try:
                v_alliance = soup.find_all(
                    'a', href=re.compile('/alliance/'))[1].get_text()
                title = "[Kill Alert] {0} {1} {2} owned by {3} of {4} has "\
                        "been destroyed.".format(
                            v_alliance, isk_worth, v_ship, v_pilot, v_corp)
            except IndexError:
                v_alliance = "<No Alliance>"
                title = "[Kill Alert] {0} {1} owned by {2} of {3} has "\
                        "been destroyed.".format(
                            isk_worth, v_ship, v_pilot, v_corp)
                            
            thread_info.append(title)
            thread_info.append(url)
    return(thread_info)


def create_threads(thread_info):
    '''
        -- Exclusively used by thread posting portion of bot. -- 
        Post thread(s) to desired subreddit and then waits for next loop. 
    '''
    titles, links = [], []
    x = 0
    for item in thread_info:
        if x % 2 == 0:
            titles.append(item)
        else:
            links.append(item)
        x += 1
    for thread in range(len(titles)):
        title, link = titles[thread], links[thread]
        r.submit(subreddit, title, url=link, captcha=None)


def condense_value(num, suffix='ISK'):
    '''
        condense_value() condenses the ISK (EVE-online currency) values from
        Examples such as: "123,456,789.00 ISK"
        Into neater forms such as: "123.46m ISK"
    '''
    if num > 999999999999999:
        return("%s %s") % (num, suffix)
    else:
        for unit in ['', 'k', 'm', 'b', 't']:
            if abs(num) < 1000.0:
                return "%.2f%s %s" % (num, unit, suffix)
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
                "\n\n>On {0} a{1}s piloted by {2} of ({3} | {4}) was destroyed "
                "in system {5} by {6} of ({7} | {8}) flying a{9}s along with "
                "{10} others.".format(date, v_ship_type, v_pilot_name, v_corp,
                    v_alliance, system, kb_pilot_name, kb_corp,
                    kb_alliance, kb_ship_type, other_pilots))
        else:
            kb_pilot_name = soup.find_all('td', style="text-align: center;")[0]
            kb_pilot_name = kb_pilot_name.find_all(
                'a', href=re.compile('/character/'))[0].img.get('alt')
            people_data = (
                "\n\n>On {0} a{1}s piloted by {2} of ({3} | {4}) was destroyed "
                "in system {5} by {6}s flying a{7}s along with {8} "
                "other".format(date, v_ship_type, v_pilot_name, v_corp,
                    v_alliance, system, kb_pilot_name,
                    kb_ship_type, other_pilots))
            if int(other_pilots) == 1:
                people_data += "."
            else:
                people_data += "s."
            reply_data.append(people_data)
        reply_data.append(
            "\n\n>Value dropped: {0}\n\n>Vale destroyed: {1}\n\n>Total value: "
            "{2}\n\n>[{3}'s {4}]({5})\n\n".format(isk_dropped, isk_destroyed,
                isk_total, v_pilot_name, v_rigging_text, v_rigging_link)
                + ('-'*50))
    reply_data = ('\n\n'.join(reply_data))

    # Part 4
    msg_bot_link = 'http://www.reddit.com/message/compose?to=Killmail_Bot'
    github_link = 'https://github.com/ArnoldM904/' \
                  'EK_Reddit_Bot/blob/master/EKR_Bot.py'

    return(
        "Hi, I am a killmail reader bot. "
        "Let me summarize that for you!" +
        reply_data +
        "\n\n^^This ^^bot ^^is ^^open ^^source ^^& ^^in ^^active "
        "^^development! ^^Please ^^feel ^^free ^^to ^^contribute: ^^["
        "Suggestions]({0}) ^^| ^^[Code]({1})").format(msg_bot_link, github_link)

def post_replies():
    ''' 
        run_reply_function() consists of 7 main parts that push the bot through its main
        processes.

        Part 1. Open and read cache file of recorded comments replied to.
        Part 2. Go to the subreddit and check the latest 150 comments.
        Part 3. Find comments containing zkillboard.com links and set them
                apart.
        Part 4. Check that killmails is not empty and comments have not
                already been replied to using the cache.
        Part 5. Save comment ID into cache.
        Part 6. Send zkillboard URL into read_killmail()
        Part 7. Reply to comment.
    '''
    # Part 1
    with open('cache.txt', 'r') as cache:
        existing = cache.read().splitlines()

    # Part 2
    comments = subreddit.get_comments(limit=150)

    with open('cache.txt', 'a+') as cache:
        for comment in comments:
            comment_text = comment.body.lower()

            # Part 3
            killmails = [
                item for item in comment_text.split()
                #Get the link, and add it to the list if +nokmbot is not present in the comment.
                if re.match(r"https://zkillboard\.com/kill/*", item) 
                and not re.match(r"\+nokmbot", item)]

            # Part 4
            if not(killmails and comment.id not in existing):
                continue

            mails = []
            for mail in killmails:
                # Check that the end of the killmail URL is not corrupted.
                # (IE: Prevent 'zkillboard.com/kill/123.') from crashing
                # the program.
                if mail.startswith('https://zkill') or \
                   mail.startswith('http://zkill'):
                    if mail[-1:] in '1234567890/':
                        mails.append(mail)
            existing.append(comment.id)
            # Part 5
            cache.write(comment.id + '\n')
            print("I found a new comment! The ID is: " + comment.id)
            # Part 6
            report = read_killmail(mails)
            # Part 7
            comment.reply(report)

def post_threads():
    '''
        -- Exclusively used by thread posting portion of bot. -- 
        Initiate the bot to go through the thread posting functions.
    '''
    create_threads(
        analyze_kills(
            check_cache(
                find_kills())))


while True:
    try:
        post_replies()
        post_threads()
    except requests.ConnectionError as e:
        print(e)
    loop_count += 1
    print("Program loop #{0} completed successfully.".format(loop_count))
    time.sleep(1200)
