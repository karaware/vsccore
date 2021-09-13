#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import operation_redis
import requests
import io
import datetime

def upload_graph(graphImgName):
    bucket = "vsc-graph"
    filePath = "/root/vtuber/vsc/realtime_livedata/img/" + graphImgName

    s3Key = "njiro/" + graphImgName
    #s3Key = "tomeru/" + graphImgName

    s3 = boto3.resource("s3")
    s3.Bucket(bucket).upload_file(Filename=filePath, Key=s3Key)


def upload_thumbnail(currentVideoId, currentThumbnailsUrl):
    res = requests.get(currentThumbnailsUrl)
    res.raise_for_status()

    img = io.BytesIO(res.content)

    dtNow = datetime.datetime.now()
    strDtNow = dtNow.strftime("%Y%m%d_%H%M")

    thumbnailImgName = strDtNow + "_" + currentVideoId + "_thumbnail.jpg"
    s3Key = "njiro/" + thumbnailImgName
    #s3Key = "tomeru/" + thumbnailImgName

    s3 = boto3.client('s3')
    s3.upload_fileobj(img, "vsc-thumbnail", s3Key)


