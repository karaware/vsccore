#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import redis
import timezone
import datetime
import ast

def set_upcoming_stream(youtube, videoIdLists):
    r = redis.Redis(host='localhost', port=6379, db=1)

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
    r = redis.Redis(host='localhost', port=6379, db=1)

    keys = r.keys("*")
    #print(keys)

    streamInfoLists = []

    for key in keys:
        streamInfo = ast.literal_eval(r.get(key).decode())
        streamInfoLists.append(streamInfo)

    streamInfoLists.sort(reverse=False, key=lambda e: e["scheduledStartTime"])

    nextStream = streamInfoLists[0]

    #print(json.dumps(nextStream, indent=2, ensure_ascii=False))

    r = redis.Redis(host='localhost', port=6379, db=2)

    r.set("videoId", nextStream["videoId"])
    r.set("title", nextStream["title"])
    r.set("thumbnailsUrl", nextStream["thumbnailsUrl"])
    r.set("scheduledStartTime", nextStream["scheduledStartTime"])


def get_next_stream():
    r = redis.Redis(host='localhost', port=6379, db=2)
    keys = r.keys("*")

    nextStream = {}

    for key in keys:
        #print(key)
        #print(r.get(key).decode())
        nextStream[key.decode()] = r.get(key).decode()
        #nextStream.append(r.get(key).decode())

    #print(json.dumps(nextStream, indent=2, ensure_ascii=False))
    return nextStream


def flush_db_1():
    r = redis.Redis(host='localhost', port=6379, db=1)
    r.flushdb()


def flush_db_2():
    r = redis.Redis(host='localhost', port=6379, db=2)
    r.flushdb()


def flush_db_3():
    r = redis.Redis(host='localhost', port=6379, db=3)
    r.flushdb()



