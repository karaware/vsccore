#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import redis
import datetime
import timezone
import ast
import log_vsc

logger = log_vsc.logger_set()

def rpush_viewers_record(videoDetailData):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    dtNow = datetime.datetime.now()
    strDtNow = dtNow.strftime('%H:%M')
    if "concurrentViewers" in videoDetailData["liveStreamingDetails"]:
        r.rpush("timeRecord", strDtNow)
        r.rpush("viewersRecord", videoDetailData["liveStreamingDetails"]["concurrentViewers"])


def set_current_live_status(currentLiveStatus):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("currentLiveStatus", currentLiveStatus)


def set_current_viewers(currentViewers):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("currentViewers", currentViewers)


def get_current_viewers():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    currentViewers = r.get("currentViewers").decode()
    return currentViewers


def set_max_viewers(maxViewers):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("maxViewers", maxViewers)


def get_max_viewers():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    maxViewers = r.get("maxViewers").decode()
    return maxViewers


def set_current_video_id(currentVideoId):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("currentVideoId", currentVideoId)


def get_current_video_id():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    currentVideoId = r.get("currentVideoId").decode()
    return currentVideoId


def get_current_thumbnail_url():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    currentThumbnailsUrl = r.get("thumbnailsUrl").decode()
    return currentThumbnailsUrl


def set_current_title(currentTitle):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("currentTitle", currentTitle)


def get_current_title():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    currentTitle = r.get("currentTitle").decode()
    return currentTitle


def set_current_like_count(currentLikeCount):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("currentLikeCount", currentLikeCount)


def get_current_like_count():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    currentLikeCount = r.get("currentLikeCount").decode()
    return currentLikeCount


def set_actual_start_time(videoDetailData):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    jstActualStartTime = timezone.utc_to_jst(videoDetailData["liveStreamingDetails"]["actualStartTime"])
    r.set("actualStartTime", jstActualStartTime)
    logger.log(10, 'jstActualStartTime : ' + jstActualStartTime)


def get_actual_start_time():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    actualStartTime = r.get("actualStartTime").decode()
    return actualStartTime


def set_actual_end_time(videoDetailData):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    jstActualEndTime = timezone.utc_to_jst(videoDetailData["liveStreamingDetails"]["actualEndTime"])
    r.set("actualEndTime", jstActualEndTime)
    logger.log(10, 'jstActualEndTime : ' + jstActualEndTime)


def get_actual_end_time():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    actualEndTime = r.get("actualEndTime").decode()
    return actualEndTime


def get_current_live_status():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    try:
        currentLiveStatus = r.get("currentLiveStatus").decode()
    except:
        print("currentLiveStatus was not found")
        currentLiveStatus = "none"

    return currentLiveStatus


def set_end_flag_true():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("endFlag", "true")


def get_end_flag():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    try:
        endFlag = r.get("endFlag").decode()
    except:
        print("endFlag was not found")
        endFlag = "false"
        r.set("endFlag", endFlag)

    return endFlag


def get_scheduled_start_time():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=2)
    try:
        scheduledStartTime = r.get("scheduledStartTime").decode()
    except:
        print("scheduledStartTime was not found")
        scheduledStartTime = "none"

    return scheduledStartTime


def set_upcoming_stream(youtube, videoIdLists):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=1)

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
            print("streamInfoDatetime < nowDatetime")
            continue
        else:
            streamInfo["videoId"] = videosResponse["items"][0]["id"]
            streamInfo["title"] = videosResponse["items"][0]["snippet"]["title"]
            #streamInfo["thumbnailsUrl"] = videosResponse["items"][0]["snippet"]["thumbnails"]["high"]["url"]
            streamInfo["thumbnailsUrl"] = videosResponse["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
            streamInfo["scheduledStartTime"] = jstScheduledStartTime

            #r.set(streamInfo["videoId"], json.dumps(streamInfo))
            r.set(streamInfo["scheduledStartTime"], json.dumps(streamInfo))


def set_next_stream(nextStream):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=1)

    keys = r.keys("*")
    #print(keys)

    streamInfoLists = []

    for key in keys:
        streamInfo = ast.literal_eval(r.get(key).decode())
        streamInfoLists.append(streamInfo)

    streamInfoLists.sort(reverse=False, key=lambda e: e["scheduledStartTime"])

    nextStream = streamInfoLists[0]

    #print(json.dumps(nextStream, indent=2, ensure_ascii=False))

    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=2)

    r.set("videoId", nextStream["videoId"])
    r.set("title", nextStream["title"])
    r.set("thumbnailsUrl", nextStream["thumbnailsUrl"])
    r.set("scheduledStartTime", nextStream["scheduledStartTime"])


def get_next_stream():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=2)
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
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=1)
    r.flushdb()


def flush_db_2():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=2)
    r.flushdb()


def flush_db_3():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.flushdb()


def get_time_record():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)

    timeLists = r.lrange("timeRecord", 0, -1)
    strTimeLists = []

    for byteTime in timeLists:
        strTimeLists.append(byteTime.decode())

    return strTimeLists


def get_viewers_record():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)

    viewerLists = r.lrange("viewersRecord", 0, -1)
    intViewerLists = []

    for byteViewer in viewerLists:
        intViewerLists.append(int(byteViewer.decode()))

    return intViewerLists


def set_thumbnail_img_name(thumbnailImgName):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("thumbnailImgName", thumbnailImgName)


def get_thumbnail_img_name():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    thumbnailImgName = r.get("thumbnailImgName").decode()
    return thumbnailImgName


def set_graph_img_name(graphImgName):
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    r.set("graphImgName", graphImgName)


def get_graph_img_name():
    r = redis.Redis(host='vsc-redis-001.amt4dg.0001.apne1.cache.amazonaws.com', port=6379, db=3)
    graphImgName = r.get("graphImgName").decode()
    return graphImgName





