#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import timezone
import operation_redis

def get_video_detail(youtube, videoInfo):
    response = youtube.videos().list(
        part='id,snippet,liveStreamingDetails,statistics', 
        id=videoInfo["id"]["videoId"]
    ).execute()

    videoDetailData = response['items'][0]
    print(json.dumps(videoDetailData, indent=2, ensure_ascii=False))

    return videoDetailData
