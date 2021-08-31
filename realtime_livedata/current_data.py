#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operation_redis

def set_current_data(videoDetailData):

    operation_redis.rpush_viewers_record(videoDetailData)

    try:
        currentViewers = videoDetailData["liveStreamingDetails"]["concurrentViewers"]
        operation_redis.set_current_viewers(currentViewers)
    except:
        print("concurrentViewers was not found")

    currentVideoId = videoDetailData["id"]
    operation_redis.set_current_video_id(currentVideoId)

    currentTitle = videoDetailData["snippet"]["title"]
    operation_redis.set_current_title(currentTitle)

    currentLikeCount = videoDetailData["statistics"]["likeCount"]
    operation_redis.set_current_like_count(currentLikeCount)

    try:
        oneBeforeCurrentViewers = int(operation_redis.get_current_viewers())
        print(oneBeforeCurrentViewers)
        currentViewers = int(videoDetailData["liveStreamingDetails"]["concurrentViewers"])
        print(currentViewers)

        if oneBeforeCurrentViewers < currentViewers:
            maxViewers = currentViewers
        else:
            maxViewers = oneBeforeCurrentViewers

        operation_redis.set_max_viewers(maxViewers)
    except:
        print("concurrentViewers or oneBeforeCurrentViewers was not found")









