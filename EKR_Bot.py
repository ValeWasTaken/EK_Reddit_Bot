# !! Note: !! This program currently does not have Reddit interaction enabled. This is only the web-scraped information half.



# EVE: Online Killmail Reddit Bot (EKRB)
# Created by: Reddit.com/u/Valestrum
# Contribute to the open source project here: https://github.com/ArnoldM904/EK_Reddit_Bot

import urllib # Access internet and make network requests
import re  # Regex

killmail = raw_input("Enter zkillboard link: ")
url = [killmail]
i = 0
iskDroppedSource = '<td class="item_dropped">(.+?)</td>' # Gets whatever is inbetween the tags
iskDestroyedSource = '<td class="item_destroyed">(.+?)</td>'
iskTotalSource = '<strong class="item_dropped">(.+?)</strong>'

iskDroppedText = re.compile(iskDroppedSource) # Converts above regex string into something that can be interpreted by regular library
iskDestroyedText = re.compile(iskDestroyedSource)
iskTotalText = re.compile(iskTotalSource)

htmlfile = urllib.urlopen(url[i])
htmltext = htmlfile.read()

iskDropped = re.findall(iskDroppedText,htmltext)
iskDestroyed = re.findall(iskDestroyedText,htmltext)
iskTotal = re.findall(iskTotalText,htmltext)

print("Hi, I am a killmail reader bot. Let me summarize this killmail for you!")
print("Value dropped: " + str(iskDropped[0]))
print("Value destroyed: " + str(iskDestroyed[0]))
print("Total value: " + str(iskTotal[0]))
print("^^This ^^bot ^^is ^^brand ^^new ^^please ^^be ^^gentle. ^^PM ^^for ^^questions.")
