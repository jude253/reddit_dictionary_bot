# reddit_dictionary_bot
This bot searchs through a bunch of comments on reddit and when it finds a comment says "define &lt;word>" it is going to reply to that comment with the definition of &lt;word>.  It used the praw reddit package for python and reddit APIs to get the reddit posts, comments, reply, etc... and the oxford dictionary API to define the word.


Right now (8/18/2018) 

Issue 1: When the bot gets <word> that is both a noun and a verb like for example "changes". 

Solution 1: use POS tagging to get this info. (this sounds better long term)

Solution 2: find the first verb definition and the first noun definition (if they exist) and put those in the reply comment


Issue 2: Parsing the definition response JSON from the OXFORD DICTIONARY API can sometimes have strange formats

Solution: more investigating of the response format


Issue 3: how do I decide which comments to search on a given post?

Solution: I think I should search all the comments that are visible to the user when they first load the page (not those that require clicking on the "more comments" text.  Otherwise it would take too long to go through all the comments, and no one would see the bot's response with the definition anyway.
