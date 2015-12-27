EK_Reddit_Bot
=============

EVE: Online Killmail Reddit Bot (EKRB)

EKRB is a web-scraping bot has two core functions. The first is it searches the <a href="http://www.reddit.com/r/eve">/r/eve sub-reddit</a> for posts containing zkillboard.com killmail links before posting a reply to said post with the summary of the killmail. This bot is primarily for mobile phone / tablet users who would otherwise be too inconvienced to view a killmail link or links, users with low connection speeds who load killmail pages very slowly, and PC users who would simply rather quickly see the gist of the information rather than clicking 10 different links alike. 

The second function being it detects any kills on zkillboard.com worth 20 billion or more ISK and then posts a thread onto the /r/eve subreddit with the core information as the title.

EKRB is still in active development and could very much use any help, please feel free to look over the code, ask questions, and help improve it. :)

Version 2.0.45 supports zkillboard and posts the following information:
- ISK Dropped
- ISK Destroyed
- Total ISK
- Names of both victim and pilot scoring the killing blow and their ships
- The number of pilots involved
- The system the kill took place in
- The fitting of the victim's ship
- Date of kill
- Corp and alliance information for victim and pilot scoring killing blow
- Recognization of the "+nokmbot" phrase in comments to skip a Killmail_Bot response. 

Screenshot example of function one (post reply):
<img src="http://i.imgur.com/pHgPJDN.png"</img>

Screenshot example of function two (post thread):
<img src="http://i.imgur.com/XosUdyn.png"</img>

More features will be added in the future if desired.
Please see the attached <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/Notes.txt">Notes.txt</a> file for more information.

To begin contributing see: <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/How_to_contribute.md">How_to_contribute.md</a> !
