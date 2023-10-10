import pandas as pd
import praw
import datetime as dt
import os
import time


def get_date(created):
    return dt.datetime.fromtimestamp(created)

def get_posts(subreddit_name, query=None, filter_name=None, limit=None):

    LIMIT = 1000
    
    if limit != None:
        LIMIT = limit

    #configure OAuth
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='',
                         username='',
                         password='')

    #initialtize subreddit object
    subreddit = reddit.subreddit(subreddit_name)


    #error handling

    if query==None and filter_name==None:

        print("You must specify a query or a filter")

    else:

        if query=None:

            FILENAME = subreddit_name + "_" + filter_name + ".xlsx"

            print("Pulling posts by subreddit filter " + filter_name + ". Not searching for any specific term.")

            if filter_name.lower() == "hot":

                subreddit = subreddit.hot(limit=LIMIT)

            if filter_name.lower() == "new":

                subreddit = subreddit.new(limit=LIMIT)

            if filter_name.lower() == "controversial":

                subreddit = subreddit.controversial(limit=LIMIT)

            if filter_name.lower() == "top":

                subreddit = subreddit.top(limit=LIMIT)


        else:

            FILENAME = subreddit_name + "_" + query + ".xlsx"

            print("Pulling posts by a query: " + query+".")

            subreddit = subreddit.search(query, limit=LIMIT)



        data_dict = {

            "title":[],
            "score":[],
            "id":[], "url":[],
            "comms_num": [],
            "created": [],
            "body":[]

            }

        for post in subreddit:
            data_dict["title"].append(post.title)
            data_dict["score"].append(post.score)
            data_dict["id"].append(post.id)
            data_dict["url"].append(post.url)
            data_dict["comms_num"].append(post.num_comments)
            data_dict["created"].append(post.created)
            data_dict["body"].append(post.selftext)
            time.sleep(0.1)
            

        df= pd.DataFrame(data_dict)

        _timestamp = df["created"].apply(get_date)

        hot_topics_data = df.assign(timestamp = _timestamp)

        df.drop(columns=['created'],inplace=True)

        df.to_excel(FILENAME)


get_posts(subreddit_name="pastry", query="brioche", limit=500)
get_posts(subreddit_name="pastry", filter_name="controversial", limit=100)




