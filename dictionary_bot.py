#!/usr/bin/python
import praw
import pdb
import re
import os
import time
import requests
import json

# api junk:
app_id = '03cecbef'
app_key = 'cd0910e09f829a72c5334baa50f3b5e3'


language = 'en'         #language code for API
word_id = 'cow'      #word that's being retrieved from the dictionary
json_from_API = ''      #initialization of the storage variable
comment_text = ''       #initialize the comment definition response, eventually this will have the comment in it
#set up the API endpoint:
url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()


#bot junk:
subreddit_name = 'pythonforengineers'
post_search_criteria = ""
comment_search_string = "hello"
bot_name = "bot1"
bots = ["bot0","bot1","bot2","bot3","bot4","bot5"]
subreddit_name = 'pythonforengineers'
posts_replied_to = []
comments_replied_to = []
limit_of_comment_replies = 2
limit_of_comments_searched = 10
limit_of_posts_searched = 2
word_to_be_defined = ''

def define(word):
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    if r.status_code == 200: #only run the rest of the script if the word exists and the api works
        json_from_API = json.loads(json.dumps(r.json()))
    
        comment_text = json_from_API['results'][0]["id"] + "\n\n"
    #everything is in try except so that if the entries don't exist the bot wont crash
        try:
        #the definition then 2 new lines
            comment_text += "\t definition: " + json_from_API['results'][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
            comment_text += "\n\n"
        except:
            pass

        try:
        #example sentence
            comment_text += "\t example: " + json_from_API['results'][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"]
        except:
            pass
        print(comment_text)
        return comment_text
#submission = post
#comment = comment on post


def main():
    #post_tracking_file_opener()
    
        
    
    reddit = praw.Reddit(bots[0])
    subreddit = reddit.subreddit(subreddit_name)
    submission_handling_without_repeat_safety(posts_replied_to,subreddit,bots[0])

  

    
    

    #post_tracking_file_closer()


def comment_handling(comments):
    comments_replied_number = 0
    comments_searched = 0
    global words
  
    for comment in comments:
        if comments_searched == limit_of_comments_searched:
            print("limit of comments searched reached")
            break
         
        #search criteria, no duplicate replies, limit of replies 
        if  re.search(comment_search_string, comment.body, re.IGNORECASE) and \
            comment.id not in comments_replied_to and \
            comments_replied_number < limit_of_comment_replies:
            #do whatever

            


            #comment.reply("ww says hi")
            print(comment.body)
            #splits all the words in the post up so I can get the word after searched word ie define
            list_of_words_from_comment = comment.body.split()
            prev_word = ''
            for word in list_of_words_from_comment:
                if prev_word == comment_search_string:
                    word_to_be_defined = word
                    #print(word_to_be_defined)
                    comment.reply(define(word_to_be_defined))
                prev_word = word

            #print("Bot saw on: ", comment.id)
            #comments_replied_number += 1
            comments_replied_to.append(comment.id)
        comments_searched += 1

def submission_handling(posts_replied_to,subreddit,bot):
    for submission in subreddit.hot(limit=limit_of_posts_searched):
        if  not submission.archived and \
            submission.id not in posts_replied_to and \
            re.search(post_search_criteria, submission.title, re.IGNORECASE):
            #submission.reply("hello this is " + bot)
            print(bot + " in: ", submission.title)
            

            all_comments = submission.comments.list()
            comment_handling(all_comments)
            posts_replied_to.append(submission.id)

def submission_handling_without_repeat_safety(posts_replied_to,subreddit,bot):
    for submission in subreddit.hot(limit=limit_of_posts_searched):
        if  not submission.archived and \
            re.search(post_search_criteria, submission.title, re.IGNORECASE):
            #submission.reply("hello this is " + bot)
            print(bot + " in : ", submission.title)

            #save comments and send them to the comment handling method:
            all_comments = submission.comments.list()
            comment_handling(all_comments)
            posts_replied_to.append(submission.id)

def post_tracking_file_opener():
    global posts_replied_to
    #setting up a file to keep track of what posts have already been commented on
    if not os.path.isfile("posts_replied_to_" + bot_name + ".txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to_" + bot_name + ".txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

def post_tracking_file_closer():
    with open("posts_replied_to_" + bot_name + ".txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
def comment_tracking_file_closer():
    with open("comments_replied_to_" + bot_name + ".txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")

def submission_handling(subreddit):
    for submission in subreddit.hot(limit=limit_of_posts_searched):

        #post not archived, no duplicate replies, search criteria 
        if  not submission.archived and \
            submission.link_flair_text != "Modpost" and\
            submission.id not in posts_replied_to and \
            re.search(post_search_string, submission.title, re.IGNORECASE):
            print("Bot in: ", submission.title)
            #do whatever
            #print(vars(submission))
            #submission.reply("hi")
            
            all_comments = submission.comments.list()
            comment_handling(all_comments)
            posts_replied_to.append(submission.id)

if __name__ == '__main__':
    main()