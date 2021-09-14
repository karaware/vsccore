#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apiclient.discovery import build
import datetime
import variable

def get_videoid(youtube, channelId):
    searchResponse = youtube.search().list(
        part = "snippet",
        channelId = variable.channelId,
        type = "video",
        eventType = "upcoming",
        maxResults = 50,
        order = "date" #日付順にソート
    ).execute()

    videoIdLists = []
 
    for item in searchResponse.get("items", []):
        videoIdLists.append(item["id"]["videoId"])

    return videoIdLists
