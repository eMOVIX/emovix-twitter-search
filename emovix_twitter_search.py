__author__ = 'Jordi Vilaplana'

import tweepy
import pymongo
from pymongo import MongoClient
import json
import logging
import time
import datetime

logging.basicConfig(filename='emovix_twitter_search.log',level=logging.WARNING)

# Configuration parameters
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
database_name = ""

client = None
db = None

if __name__ == '__main__':
    logging.debug('emovix_twitter_search.py starting ...')

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']
        database_name = config['database_name']

    client = MongoClient('mongodb://localhost:27017/')
    db = client[database_name]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    while True:
        # Queries to the Twitter Search API are limited to 1 every 5 seconds, approximately
        # https://dev.twitter.com/rest/public/rate-limits
        time.sleep(5)

        # The enabled user with the oldest update time is selected
        twitter_user = db.twitterUserMonitor.find_one({ 'enabled': True }, sort=[("last_updated", pymongo.ASCENDING)])

        # Check if there is at least one enabled user
        if twitter_user == None:
            logging.debug('No users to update.')
            continue

        # If the last update was less than 1 day ago, it won't be updated again
        days_since_update = (datetime.datetime.now() - twitter_user['last_updated']).days

        if days_since_update < 1:
            logging.debug('All users already up to date.')
            continue

        try:
            # Fetch user information from the Twitter Public API
            user = api.get_user(twitter_user['screen_name'])
            logging.debug('Fetching information from Twitter user @' + user.screen_name + ' ...')

            # JSON object with the parameters that will be saved to the database
            user_json = { 'id': user.id,
                          'screen_name': user.screen_name,
                          'description': user.description,
                          'favourites_count': user.favourites_count,
                          'followers_count': user.followers_count,
                          'friends_count': user.friends_count,
                          'lang': user.lang,
                          'listed_count': user.listed_count,
                          'location': user.location,
                          'name': user.name,
                          'statuses_count': user.statuses_count,
                          'url': user.url}

            # Insert the Twitter user snapshot into the database
            db.twitterUserSnapshot.insert_one(user_json)
            logging.debug('New user snapshot inserted.')

            # Update the last updated information for this user
            db.twitterUserMonitor.update_one({ '_id': twitter_user['_id']}, { '$set': { 'last_updated': datetime.datetime.now() } })

        except Exception as e:
            # Oops
            logging.error(e.__class__)
            logging.error(e)

            # Check if user no longer exists
            if int(e.message[0]['code']) == 34:
                logging.error('Twitter user ' + twitter_user['screen_name'] + ' no longer exists.')
                # Further automatic data collection for this user is disabled
                db.twitterUserMonitor.update_one({ '_id': twitter_user['_id']}, { '$set': { 'enabled': False } })

            # Ignore other exceptions
            continue
        except KeyboardInterrupt:
            break
