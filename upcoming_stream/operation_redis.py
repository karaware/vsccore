#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import redis
import timezone
import datetime
import ast
import log_vsc

def set_upcoming_stream(youtube, videoIdLists):
    logger = log_vsc.logger_set()

    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=7)

    for videoId in videoIdLists:
        videosResponse = youtube.videos().list(
            part = "snippet, liveStreamingDetails",
            id = videoId
        ).execute()

        #print(json.dumps(videosResponse, indent=2, ensure_ascii=False))

        streamInfo = {}

        utcScheduledStartTime = videosResponse["items"][0]["liveStreamingDetails"]["scheduledStartTime"]
        jstScheduledStartTime = timezone.utc_to_jst(utcScheduledStartTime)

        nowDatetime = datetime.datetime.now()

        streamInfoDatetime = datetime.datetime.strptime(jstScheduledStartTime, "%Y/%m/%d %H:%M:%S")
        #print(streamInfoDatetime)
        #print(nowDatetime)
        #print(str(streamInfoDatetime < nowDatetime))
        if streamInfoDatetime < nowDatetime:
            continue
        else:
            streamInfo["videoId"] = videosResponse["items"][0]["id"]
            streamInfo["title"] = videosResponse["items"][0]["snippet"]["title"]
            streamInfo["thumbnailsUrl"] = videosResponse["items"][0]["snippet"]["thumbnails"]["high"]["url"]
            streamInfo["scheduledStartTime"] = jstScheduledStartTime

            #r.set(streamInfo["videoId"], json.dumps(streamInfo))
            r.set(streamInfo["scheduledStartTime"], json.dumps(streamInfo))


def set_next_stream(nextStream):
    logger = log_vsc.logger_set()

    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=7)

    keys = r.keys("*")
    #print(keys)

    streamInfoLists = []

    for key in keys:
        streamInfo = ast.literal_eval(r.get(key).decode())
        streamInfoLists.append(streamInfo)

    streamInfoLists.sort(reverse=False, key=lambda e: e["scheduledStartTime"])

    print(streamInfoLists)
    logger.log(10, streamInfoLists)

    try:
        nextStream = streamInfoLists[0]
    except:
        print('next_stream not found')
        logger.log(10, 'next_stream not found')
        exit()

    #print(json.dumps(nextStream, indent=2, ensure_ascii=False))

    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=8)

    r.set("videoId", nextStream["videoId"])
    r.set("title", nextStream["title"])
    r.set("thumbnailsUrl", nextStream["thumbnailsUrl"])
    r.set("scheduledStartTime", nextStream["scheduledStartTime"])


def get_next_stream():
    logger = log_vsc.logger_set()

    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=8)
    keys = r.keys("*")

    nextStream = {}

    for key in keys:
        #print(key)
        #print(r.get(key).decode())
        nextStream[key.decode()] = r.get(key).decode()
        #nextStream.append(r.get(key).decode())

    #print(json.dumps(nextStream, indent=2, ensure_ascii=False))
    return nextStream

def get_current_live_status():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=9)
    try:
        currentLiveStatus = r.get("currentLiveStatus").decode()
    except:
        print("currentLiveStatus was not found")
        currentLiveStatus = "none"

    return currentLiveStatus

def flush_db_7():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=7)
    r.flushdb()


def flush_db_8():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=8)
    r.flushdb()


def flush_db_9():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=9)
    r.flushdb()



