#!/usr/bin/env python
# -*- coding: utf-8 -*-

import auth_youtube
import search_video
import operation_redis
import variable

def set_upcoming_stream():
    channelId = variable.channelId

    youtube = auth_youtube.get_object()

    videoIdLists = search_video.get_videoid(youtube, channelId)

    operation_redis.flush_db_7()

    operation_redis.set_upcoming_stream(youtube, videoIdLists)



