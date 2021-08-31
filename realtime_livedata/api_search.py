#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import operation_redis
import api_video
import tweet
import operation_redis
import live_result
import logging
import upcoming_stream
import next_stream


#def search_channel(youtube, channelId):
#    response = youtube.search().list(
#        part='id, snippet',
#        channelId=channelId,
#        type='channel'
#    ).execute()
#    
#    searchChannelData = response["items"][0]
#
#    operation_redis.set_current_live_status(searchChannelData)
#
#    return searchChannelData

def search_live_video(youtube, channelId):
    # ログ設定
    logger = logging.getLogger('LoggingTest')
    logger.setLevel(10)
    fh = logging.FileHandler('/home/pi/vtuber/tomeru/realtime_livedata/test.log')
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    logger.log(10, 'api_search 0')

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

            operation_redis.set_end_flag_true()
            logger.log(10, 'api_search live was finished set_end_flag_true')

            currentLiveStatus ="none"

            operation_redis.set_current_live_status(currentLiveStatus)

            logger.log(10, 'api_search 3')
            
            live_result.make_graph()
  
            logger.log(10, 'api_search 4')

            upcoming_stream.set_upcoming_stream()

            next_stream.set_next_stream()

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
            videoInfo = response["items"][0]
            tweet.start_tweet(videoInfo)
            operation_redis.flush_db_3()

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

