#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests
from io import BytesIO
import redis
import operation_redis
import variable

#def start_tweet(videoInfo, currentInfo):
def start_tweet(videoInfo):
    #CK = 'tXwiA2Zh5sSlwwE78ld07Qfyf'
    #CS = '5S9pL9GNB0vhTIcXNMMoEdPri59gWMeJ7CYwVAoDSFIZHMAZtS'
    #AT = '1423185548177408001-QpgAThSxWd7xaN5gMaFQKoeyuyUCcI'
    #AS = 'nq1Pf3huJeB3WqYr8MO2hBDovmFtmbjLQzquaILo5oTBi'

    #auth = tweepy.OAuthHandler(CK, CS)
    #auth.set_access_token(AT, AS)

    auth = tweepy.OAuthHandler(variable.CK, variable.CS)
    auth.set_access_token(variable.AT, variable.AS)
    api = tweepy.API(auth)

    #api.update_status("tweetを投稿")

    #message = "以下のURLで #息根とめる が配信中!\n"
    message = "#息根とめる が配信中!\n"
    #message = "test\n"
    message += videoInfo["snippet"]["title"] + "\n"
    #message += "https://www.youtube.com/watch?v=" + videoInfo["id"]["videoId"] + "\n"
    #message += "配信開始時間 : " + currentInfo["jstStartTime"] + "\n"
    #message += "現在の視聴者数 : " + currentInfo["currentViewer"]

    #print(videoInfo)
    #print(currentInfo)

    img = requests.get(videoInfo["snippet"]["thumbnails"]["high"]["url"]).content
    result_img = api.media_upload(filename='img.png', file=BytesIO(img))
    tweet = api.update_status(status=message, media_ids=[result_img.media_id])


def result_tweet(imgPath):
    CK = 'tXwiA2Zh5sSlwwE78ld07Qfyf'
    CS = '5S9pL9GNB0vhTIcXNMMoEdPri59gWMeJ7CYwVAoDSFIZHMAZtS'
    AT = '1423185548177408001-QpgAThSxWd7xaN5gMaFQKoeyuyUCcI'
    AS = 'nq1Pf3huJeB3WqYr8MO2hBDovmFtmbjLQzquaILo5oTBi'

    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)

    currentVideoId = operation_redis.get_current_video_id()
    currentTitle = operation_redis.get_current_title()
    currentLikeCount = operation_redis.get_current_like_count()
    maxViewers = operation_redis.get_max_viewers()

    #message = "test\n"
    message = "本日の #息根とめる の配信記録\n"
    message += currentTitle + "\n"
    #message += "https://www.youtube.com/watch?v=" + currentVideoId + "\n"
    message += "高評価数 : " + currentLikeCount + "\n"
    #message += "最高同時接続者数 : " + maxViewers + "\n"
    message += "お疲れさまでした！"

    api.update_with_media(filename=imgPath,status=message)


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

