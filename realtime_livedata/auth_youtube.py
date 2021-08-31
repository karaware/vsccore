#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from apiclient.discovery import build
import variable

def get_object():
    #API_KEY = 'AIzaSyDmJgRoehDS8xilq1ziUBTraScPYaevZq4' #vtuber-date
    #API_KEY = 'AIzaSyCdziJOaYIUEiZ5f-qTOeQBmt_4Cxucw4w' #tomerubot
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=variable.API_KEY
    )

    return youtube
