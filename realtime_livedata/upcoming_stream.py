#!/usr/bin/env python
# -*- coding: utf-8 -*-

import auth_youtube
import operation_redis
import upcoming_videoid
import variable

def set_upcoming_stream():
    youtube = auth_youtube.get_object()

    videoIdLists = upcoming_videoid.search_upcoming_videoid(youtube, variable.channelId)

    operation_redis.flush_db_1()

    operation_redis.set_upcoming_stream(youtube, videoIdLists)

#set_upcoming_stream()

