# emovix-twitter-search
Module that will periodically search and update Twitter user information.

## Project requirements

- git
- Python 2.7.10
- pip
- virtualenv [optional]
- MongoDB 3.0.5

## Project setup

Clone the project repository:

    git clone https://github.com/eMOVIX/emovix-twitter-search.git

Setup virtualenv [optional]:

    cd emovix-twitter-search
    virtualenv venv
    source venv/bin/activate

Install the requirements:

    pip install -r requirements.txt

To exit the virtualenv:

    deactivate

Edit the config.json file to add your own Twitter API credentials and the MongoDB database name:

    vim config.json

Run the program:

    python emovix_twitter_search.py

Add to supervisor:

    sudo vim /etc/supervisord.d/emovix_twitter_search.conf

Add this to the file:

```
[program:emovix_twitter_search]
directory=/opt/emovix/emovix-twitter-search
command=/opt/emovix/emovix-twitter-search/venv/bin/python emovix_twitter_search.py
autostart=true
autorestart=unexpected
redirect_stderr=True
```

    sudo supervisorctl
    supervisor> reread
    supervisor> add emovix_twitter_search
