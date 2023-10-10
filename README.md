# About

A python screenscraper for Reddit using the selenium library. The scraper searches reddit for posts that contain a user defined query.
Queries can be created via the query_builder function, allowing users to search for multiple terms, specify a custom sort (as defined by reddit's sort methods: NEW HOT, RELEVANCE etc.), and limit by a specific subreddit.

reddit.py is the first part of the screenscrape. It conducts the initial query, collecting all results returned by the search query. Reddit.py returns a CSV file that contains a url to every post (see selenium_beautifulsoup_webscraping_NEW.csv). As the screenscrape takes place, it's written directly to CSV.

reddit_pull_post_text.py is the second part of the screenscrape. It loops through the post_urls from the previously rendered CSV file, collecting post text and the subreddit flair (if there is one).

The final data is returned as an excel file (see reddit_scrape_with_text.xlsx). The final data contains several data fields including: post text, post url, subreddit, subreddit flair, date posted, author, and author profile link.

# Notes

There is also a Reddit API, that allows users to make similar requests. This requires that users have a Reddit account and a developer key: https://github.com/reddit-archive/reddit/wiki/OAuth2

I like to use the Python Reddit API wrapper PRAW: https://praw.readthedocs.io/en/stable/

See file: reddit_api_version.py
