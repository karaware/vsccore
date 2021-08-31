#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import auth_youtube
import api_search
import api_video
import tweet
import operation_redis
import current_data
import variable

def main():
    #channelId = 'UCXYCBPWmFXbdTGD70eQe8zQ' #tomeru
    #channelId = 'UCiv5SwCP0tqIuMx6zubB73g' #njiro

    youtube = auth_youtube.get_object()

    searchLiveVideData = api_search.search_live_video(youtube, variable.channelId)

    videoDetailData = api_video.get_video_detail(youtube, searchLiveVideData)

    current_data.set_current_data(videoDetailData)

#main()
