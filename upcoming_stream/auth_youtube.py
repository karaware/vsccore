#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from apiclient.discovery import build

def get_object():
    #API_KEY = '####' #vtuber-date
    API_KEY = '####' #tomerubot
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=API_KEY
    )

    return youtube
