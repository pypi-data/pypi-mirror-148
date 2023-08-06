# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.conf import settings

CONF = getattr(settings, 'TWITTER', {})
import tweepy


class Api(object):

    def __init__(self, conf=CONF):
        self.conf = conf
        self.auth = auth = tweepy.OAuth1UserHandler(
            conf["CONSUMER_KEY"],
            conf["CONSUMER_KEY_SECRET"],
            conf["ACCESS_TOKEN"],
            conf["ACCESS_TOKEN_SECRET"]
        )
        self.api = tweepy.API(auth)

    def get_user(self, username):
        return self.api.get_user(screen_name=username)

    def get_tweets(self, uid):
        try:
            pages = tweepy.Cursor(
                self.api.user_timeline,
                id=uid,
                tweet_mode="extended",
                wait_on_rate_limit=True,
                count=200  # limit to 200 tweets per page
            ).pages()

            tweets = [page for page in pages]

        except:
            tweets = None
            pass

        return tweets

    def serialize_user(self, u):
        fs = ['id', 'name', 'screen_name', 'url', 'profile_image_url_https', 'description', 'created_at',
              'friends_count', 'favourites_count', 'followers_count', ]
        return dict([(f, getattr(u, f)) for f in fs])

    def serialize_tweet(self, t):
        fs = ['id', 'full_text', 'created_at', 'favorite_count']
        d = dict([(f, getattr(t, f)) for f in fs])
        d['user_id'] = t.user.id
        return d


def update_or_create_user(screen_name):
    api = Api()
    u = api.get_user(screen_name)
    from .models import User
    user, created = User.objects.update_or_create(screen_name=screen_name, defaults=dict(
        tid=u.id_str, name=u.name, url=u.url, avatar=u.profile_image_url_https, description=u.description,
        created_at=u.created_at, detail=api.serialize_user(u)
    ))
    return user


def sync_user_tweets(user):
    from .helper import Api
    api = Api()
    u = api.get_user(user.screen_name)
    pages = api.get_tweets(u.id_str)
    for p in pages:
        for a in p:
            user.tweets.update_or_create(
                tid=a.id_str, defaults=dict(
                    tid=a.id_str, full_text=a.full_text, created_at=a.created_at
                )
            )
