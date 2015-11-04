__author__ = 'Jordi Vilaplana'

import tweepy
import json
import logging
import time
import datetime
import csv

logging.basicConfig(filename='emovix_twitter_user_tweets.log',level=logging.INFO)

# Configuration parameters
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

client = None
db = None

twitter_accounts = [
    "PPopular", "PSOE", "socialistes_cat", "iunida", "ANOVA_irmandade", "ahorapodemos", "UPYD", "UPyDEuropa", "epp",
    "PES_PSE", "aldeparty", "europeangreens", "AllianceECR", "europeanleft", "PDE_EDP", "EUPARTYEFA", "AEMN_eu",
    "ECPM_official", "CiudadanosCs", "EuroPrimaveraIB", "vox_es"]

start_date = datetime.date(2014, 5, 10)
end_date = datetime.date(2014, 5, 25)

if __name__ == '__main__':
    logging.info('emovix_twitter_user_tweets.py starting ...')

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    while True:
        # Queries to the Twitter Search API are limited to 1 every 5 seconds, approximately
        # https://dev.twitter.com/rest/public/rate-limits
        time.sleep(10)

        # The enabled user with the oldest update time is selected
        twitter_user = twitter_accounts.pop(0)

        # Check if there is at least one enabled user
        if twitter_user == None:
            logging.info('No users to update.')
            break

        try:
            # Fetch user information from the Twitter Public API
            user = api.get_user(twitter_user)
            logging.info('Fetching information from Twitter user @' + twitter_user + ' ...')

            #initialize a list to hold all the tweepy Tweets
            alltweets = []

            #make initial request for most recent tweets (200 is the maximum allowed count)
            new_tweets = api.user_timeline(screen_name = twitter_user, count=200)

            #save most recent tweets
            alltweets.extend(new_tweets)

            #save the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            #keep grabbing tweets until there are no tweets left to grab
            while len(new_tweets) > 0:
                print "getting tweets before %s" % (oldest)

                #all subsiquent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = twitter_user, count=200, max_id=oldest)

                #save most recent tweets
                alltweets.extend(new_tweets)

                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

                print "...%s tweets downloaded so far" % (len(alltweets))

            #transform the tweepy tweets into a 2D array that will populate the csv
            outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

            #write the csv
            with open('%s_tweets.csv' % twitter_user, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(["id","created_at","text"])
                writer.writerows(outtweets)

        except Exception as e:
            # Oops
            logging.error(e.__class__)
            logging.error(e)

            print e.__class__
            print e

            # Ignore other exceptions
            continue
        except KeyboardInterrupt:
            break
