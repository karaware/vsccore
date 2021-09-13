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
    except:
        print("currentViewers was not found")

    try:
        logger.log(10,"start get_current_viewers")

        oneBeforeCurrentViewers = operation_redis.get_current_viewers()

        logger.log(10, oneBeforeCurrentViewers)
        logger.log(10, type(oneBeforeCurrentViewers))
        #intCurrentViewers = int(currentViewers)

        intOneBeforeCurrentViewers = int(oneBeforeCurrentViewers)

        print(oneBeforeCurrentViewers)
        logger.log(10, "oneBeforeCurrentViewers : " + oneBeforeCurrentViewers)

        print(currentViewers)
        logger.log(10, "currentViewers : " + currentViewers)
        intCurrentViewers = int(currentViewers)

        if intOneBeforeCurrentViewers < intCurrentViewers:
            maxViewers = intCurrentViewers
            logger.log(10, "intOneBeforeCurrentViewers < intCurrentViewers")
        else:
            maxViewers = intOneBeforeCurrentViewers
            logger.log(10, "intOneBeforeCurrentViewers > intCurrentViewers")

        operation_redis.set_max_viewers(maxViewers)
    except:
        print("concurrentViewers or oneBeforeCurrentViewers was not found")
        logger.log(10, "concurrentViewers or oneBeforeCurrentViewers was not found")

    try:
        #currentViewers = videoDetailData["liveStreamingDetails"]["concurrentViewers"]
        operation_redis.set_current_viewers(currentViewers)
    except:
        print("concurrentViewers was not found")

