import tweepy
import time
import os
import sys
import json
import argparse

FOLLOWING_DIR = 'following'

# Configuration parameters
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
database_name = ""

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)
    access_token = config['access_token']
    access_token_secret = config['access_token_secret']
    consumer_key = config['consumer_key']
    consumer_secret = config['consumer_secret']
    database_name = config['database_name']

enc = lambda x: x.encode('ascii', errors='ignore')

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

cursor = None
f_ids = []

def get_follower_ids(user_id):
    try:
        userfname = os.path.join('twitter-users', str(user_id) + '.json')
        if os.path.exists(userfname):
            print "A file with this user id already exists"
            return 0

        print 'Retrieving user details for twitter id %s' % str(user_id)

        try:
            user = api.get_user(user_id)
            #tweepy_cursor = tweepy.Cursor(api.followers_ids, user.screen_name, cursor="1485211686102812068").pages()
            tweepy_cursor = tweepy.Cursor(api.followers_ids, user.screen_name).pages()

            while True:
                page = tweepy_cursor.next()
                if not page:
                    break
                cursor = tweepy_cursor.next_cursor
                f_ids.extend(page)
                print "Got " + str(len(f_ids)) + " so far ..."
                time.sleep(60)

            #for page in tweepy.Cursor(api.followers_ids, user.screen_name).pages():
            #    f_ids.extend(page)
            #    print "Got " + str(len(f_ids)) + " so far ..."
            #    time.sleep(60)

            d = {'name': user.name,
                 'screen_name': user.screen_name,
                 'id': user.id,
                 'friends_count': user.friends_count,
                 'followers_count': user.followers_count,
                 'followers_ids': f_ids}

            with open(userfname, 'w') as outf:
                outf.write(json.dumps(d, indent=1))

            user = d
        except tweepy.TweepError, error:
            print type(error)

            if str(error) == 'Not authorized.':
                print 'Can''t access user data - not authorized.'
                return 0

            if str(error) == 'User has been suspended.':
                print 'User suspended.'
                return 0

            errorObj = error[0][0]

            print errorObj

            if errorObj['message'] == 'Rate limit exceeded':
                print 'Rate limited. Sleeping for 10 seconds.'
                time.sleep(10)

            return 0

    except Exception, error:
        print 'Error retrieving followers for user id: ', user_id
        print error

        print "Last cursor:"
        print cursor

        print "Performing emergency backup ..."
        if os.path.exists('twitter-users', str(user_id) + '_backup.txt'):
            with open(os.path.join('twitter-users', str(user_id) + '_backup.txt'), 'a') as outf:
                for item in f_ids:
                    outf.write("  %s,\n" % item)
        else:
            with open(os.path.join('twitter-users', str(user_id) + '_backup.txt'), 'w') as outf:
                for item in f_ids:
                    outf.write("  %s,\n" % item)

        sys.exit(1)

    return 0

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
    args = vars(ap.parse_args())

    twitter_screenname = args['screen_name']
    matches = api.lookup_users(screen_names=[twitter_screenname])

    if len(matches) == 1:
        print get_follower_ids(matches[0].id)
    else:
        print 'Sorry, could not find twitter user with screen name: %s' % twitter_screenname
