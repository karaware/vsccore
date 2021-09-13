#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apiclient.discovery import build
import datetime

def search_upcoming_videoid(youtube, channelId):
    searchResponse = youtube.search().list(
        part = "snippet",
        channelId = channelId,
        type = "video",
        eventType = "upcoming",
        maxResults = 50,
        order = "date" #日付順にソート
    ).execute()

    videoIdLists = []
 
    for item in searchResponse.get("items", []):
        videoIdLists.append(item["id"]["videoId"])

    #print(videoIdLists)

    return videoIdLists
