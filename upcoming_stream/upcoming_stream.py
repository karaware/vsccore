#!/usr/bin/env python
# -*- coding: utf-8 -*-

import auth_youtube
import search_video
import operation_redis

def set_upcoming_stream():
    #channelId = 'UCXYCBPWmFXbdTGD70eQe8zQ' #tomeru
    channelId = 'UCiv5SwCP0tqIuMx6zubB73g' #njiro

    youtube = auth_youtube.get_object()

    videoIdLists = search_video.get_videoid(youtube, channelId)

    operation_redis.flush_db_1()

    operation_redis.set_upcoming_stream(youtube, videoIdLists)



