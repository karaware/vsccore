#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import operation_redis
import api_video
import tweet
import live_result
import log_vsc
import upcoming_stream
import next_stream
import operation_s3
import datetime
import timezone
import operation_mysql

def search_live_video(youtube, channelId):

    logger = log_vsc.logger_set()

    response = youtube.search().list(
        part = "id, snippet",
        channelId = channelId,
        type = "video",
        eventType = "live"
    ).execute()
    
    print(json.dumps(response, indent=2, ensure_ascii=False))


    oneBeforeLiveStatus = operation_redis.get_current_live_status()
    print("oneBeforeLiveStatus : " + oneBeforeLiveStatus)

    if not response["items"]:
        logger.log(10, 'api_search 1')

        if oneBeforeLiveStatus == "live":
            logger.log(10, 'api_search 2')

            print("live was finished")
            logger.log(10, 'api_search live was finished')

            dtNow = datetime.datetime.now()
            strTime = dtNow.strftime('%Y/%m/%d_%H:%M:%S')
            
            currentVideoId = operation_redis.get_current_video_id()
            videoDetailData = api_video.get_finished_video_detail(youtube, currentVideoId)

            operation_redis.set_actual_end_time(videoDetailData)

            operation_redis.set_end_flag_true()
            logger.log(10, 'api_search live was finished set_end_flag_true')

            currentLiveStatus ="none"

            operation_redis.set_current_live_status(currentLiveStatus)

            logger.log(10, 'api_search 3')
            
            live_result.make_graph()
  
            logger.log(10, 'api_search 4')

            operation_mysql.insert_result()

            try:
                upcoming_stream.set_upcoming_stream()
                next_stream.set_next_stream()
            except:
                logger.log(10, 'upcoming_stream not found')
                operation_redis.flush_db_1()
                operation_redis.flush_db_2()

            operation_redis.flush_db_3()

            exit()
        else:
            currentLiveStatus ="none"
            operation_redis.set_current_live_status(currentLiveStatus)

            print("live was not found")
            exit()

    else:

        if oneBeforeLiveStatus == "none":
            print("live was started")

            logger.log(10, 'api_search live was started')

            videoInfo = response["items"][0]

            tweet.start_tweet(videoInfo)

            #print(json.dumps(videoInfo, indent=2, ensure_ascii=False))

            videoDetailData = api_video.get_video_detail(youtube, videoInfo)
            print(videoDetailData["liveStreamingDetails"]["actualStartTime"])
            logger.log(10, 'videoDetailData["liveStreamingDetails"]["actualStartTime"] : ' + videoDetailData["liveStreamingDetails"]["actualStartTime"])
            operation_redis.set_actual_start_time(videoDetailData)

            currentVideoId = videoInfo["id"]["videoId"]

            #currentThumbnailsUrl = videoInfo["snippet"]["thumbnails"]["high"]["url"]
            currentThumbnailsUrl = videoInfo["snippet"]["thumbnails"]["medium"]["url"]
            operation_s3.upload_thumbnail(currentVideoId, currentThumbnailsUrl)

            #operation_redis.flush_db_3()

        currentLiveStatus = "live"
        operation_redis.set_current_live_status(currentLiveStatus)
        
        searchLiveVideData = response["items"][0]
        print(json.dumps(searchLiveVideData, indent=2, ensure_ascii=False))
        return searchLiveVideData


def get_video_id(youtube, channelId):
    searchResponse = youtube.search().list(
        part = "snippet",
        channelId = channelId,
        type = "video",
        eventType = "upcoming",
        maxResults = 50,
        order = "date" #日付順にソート
    ).execute()

    videoIdLists = []

    for item in searchResponse.get("items", []):
        videoIdLists.append(item["id"]["videoId"])

    #print(videoIdLists)

    return videoIdLists


