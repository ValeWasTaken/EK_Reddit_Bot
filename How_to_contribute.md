Hey there!

Glad to see you're interested in contributing, EK_Reddit_Bot could definitely use the help and it is much appreciated!
<BR></BR>
However, before you start there are a few things it would help to know:
<HR></HR>
<h4>First - Read <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/Notes.txt">Notes.txt<a/></h4>
As you may have noticed EK_Reddit_Bot has a <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/Notes.txt">Notes.txt<a/> file.
This file is up-to-date with all the current bugs that need fixing and 
all of the features already being considered or need implementing.
Take a look for yourself to see the full list of currently needed contributions. (Or add some yourself!)
<HR></HR>
<h4> Second - Depending on your contribution, fork either <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot_Safe_Test.py">EKR_Bot_Safe_Test.py</a> or the main file, <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot.py">EKR_Bot.py</a> </h4>
Depending on your change you will use one or the other. If your contribution is solely to do with zkillboard.com and non-Reddit-specific parts of the program, then you should use <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot_Safe_Test.py">EKR_Bot_Safe_Test.py</a> which is ready for instant use and does not interact with Reddit so it is safe to change the code however you like and test it. If however your contribution will involve Reddit interaction, then you should be using <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot.py">EKR_Bot.py</a> however, if you are using the later please make extra sure to read the rest of this file before trying to test the code.
<HR></HR>
<h4> Third - Install packages used in your version and make required changes to your file. </h4>
I won't get into installation guides because there are a million on the internet already, but if you are unsure where to start, all packages should be installable with <a href="https://pypi.python.org/pypi/pip/">pip</a>. Just make sure you are using Python **2.7**!

As for the required changes to your file it depends on which file from above you are testing with.
For testing <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot_Safe_Test.py">EKR_Bot_Safe_Test.py</a> all you need to know is on the last line of the file the program is called with the example line: 

<i>read_killmail(['https://zkillboard.com/kill/46955779/'])</i>

This can be changed to any other zkillboard kill or it can be several killmails at once by editing it like such:

<i>read_killmail(['https://zkillboard.com/kill/46955779/','https://zkillboard.com/kill/46939238/','https://zkillboard.com/kill/46934789/'])</i>


For testing <a href="https://github.com/ArnoldM904/EK_Reddit_Bot/blob/master/EKR_Bot.py">EKR_Bot.py</a> the steps to take are the following:
- Begin by creating a new Reddit account
- Create a text file called "user_info.txt" with the username and password on lines 1 and 2 respectively. Store this file in the same directory as EKR_Bot.py
- Change the line in the program: <i>r.get_subreddit("eve")</i> to the testing subreddit:
  - <i>r.get_subreddit("test")</i>
- Create a "cache.text" file and store it in the folder where you have EKR_Bot.py
- Create a thread on <a href="reddit.com/r/test">reddit.com/r/test</a>
- Make a comment in the thread with zkillmail link(s).
- Run the bot and wait a few seconds for the bot to detect and reply to your comment.
- Fix any bugs until your change works as intended.
  - Note: You will need to clear your cache to reply to the same comment twice. Otherwise you will need to make a new comment for the bot to reply again.

<HR></HR>
<h4> Fourth and finally, merge your change! </h4>
If you got this far you have my sincere thanks! Just write a quick description of your change and submit a merge. I will double-check the submission for any bugs and then merge your change into the main and active bot.
