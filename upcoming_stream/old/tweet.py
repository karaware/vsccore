#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests
from io import BytesIO

def tweet_next_steam(nextStream):
    CK = 'tXwiA2Zh5sSlwwE78ld07Qfyf'
    CS = '5S9pL9GNB0vhTIcXNMMoEdPri59gWMeJ7CYwVAoDSFIZHMAZtS'
    AT = '1423185548177408001-QpgAThSxWd7xaN5gMaFQKoeyuyUCcI'
    AS = 'nq1Pf3huJeB3WqYr8MO2hBDovmFtmbjLQzquaILo5oTBi'

    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)

    #api.update_status("tweetを投稿")

    message = "#息根とめる 次の配信予定\n"
    message += "開始予定時刻 : " + nextStream["scheduledStartTime"] + "\n"
    message += "タイトル : " + nextStream["title"] + "\n"
    message += "URL : https://www.youtube.com/watch?v=" + nextStream["videoId"]

    img = requests.get(nextStream["thumbnailsUrl"]).content
    result_img = api.media_upload(filename='img.png', file=BytesIO(img))
    api.update_status(status=message, media_ids=[result_img.media_id])
