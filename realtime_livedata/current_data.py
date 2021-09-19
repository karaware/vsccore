#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operation_redis
import log_vsc

def set_current_data(videoDetailData):
    logger = log_vsc.logger_set()

    operation_redis.rpush_viewers_record(videoDetailData)

#    try:
#        currentViewers = videoDetailData["liveStreamingDetails"]["concurrentViewers"]
#        operation_redis.set_current_viewers(currentViewers)
#    except:
#        print("concurrentViewers was not found")

    currentVideoId = videoDetailData["id"]
    operation_redis.set_current_video_id(currentVideoId)

    currentTitle = videoDetailData["snippet"]["title"]
    operation_redis.set_current_title(currentTitle)

    currentLikeCount = videoDetailData["statistics"]["likeCount"]
    operation_redis.set_current_like_count(currentLikeCount)

    try:
        currentViewers = videoDetailData["liveStreamingDetails"]["concurrentViewers"]
        intCurrentViewers = int(currentViewers)
        logger.log(10, "currentViewers : " + currentViewers)
        intCurrentViewers = int(currentViewers)
    except:
        print("currentViewers was not found")
        logger.log(10, "currentViewers was not found")

    try:
        maxViewers = operation_redis.get_max_viewers()
        intMaxViewers = int(maxViewers)
        logger.log(10, "maxViewers : " + maxViewers)

        if intMaxViewers < intCurrentViewers:
            intMaxViewers = intCurrentViewers
            logger.log(10, "intMaxViewers < intCurrentViewers")
            logger.log(10, "intMaxViewers : " + currentViewers)
        else:
            logger.log(10, "intMaxViewers > intCurrentViewers")
            logger.log(10, "intMaxViewers : " + maxViewers)

        operation_redis.set_max_viewers(intMaxViewers)
    except:
        print("concurrentViewers or maxViewers was not found")
        logger.log(10, "concurrentViewers or maxViewers was not found")

    try:
        #currentViewers = videoDetailData["liveStreamingDetails"]["concurrentViewers"]
        operation_redis.set_current_viewers(currentViewers)
    except:
        print("concurrentViewers was not found")

    try:
        operation_redis.get_max_viewers()
    except:
        operation_redis.set_max_viewers(int(videoDetailData["liveStreamingDetails"]["concurrentViewers"]))


