#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import operation_redis
import requests
import io
import datetime
import os

def upload_graph(graphImgName):
    bucket = "vsc-graph"
    filePath = "/home/vsc/vsccore/tomeru/realtime_livedata/img/" + graphImgName

    s3Key = "tomeru/" + graphImgName
    #s3Key = "tomeru/" + graphImgName

    operation_redis.set_graph_img_name(graphImgName)

    s3 = boto3.resource("s3")
    s3.Bucket(bucket).upload_file(Filename=filePath, Key=s3Key, ExtraArgs={"ContentType": "image/png"})
    #s3.upload_file(Filename=filePath, Bucket=bucket, Key=s3Key, ExtraArgs={"ContentType": "image/png"})


def upload_thumbnail(currentVideoId, currentThumbnailsUrl):
    res = requests.get(currentThumbnailsUrl)
    res.raise_for_status()

    img = io.BytesIO(res.content)

    dtNow = datetime.datetime.now()
    strDtNow = dtNow.strftime("%Y%m%d_%H%M")

    thumbnailImgName = strDtNow + "_" + currentVideoId + "_thumbnail.jpg"
    s3Key = "tomeru/" + thumbnailImgName
    #s3Key = "tomeru/" + thumbnailImgName

    operation_redis.set_thumbnail_img_name(thumbnailImgName)

    s3 = boto3.client('s3')
    s3.upload_fileobj(img, "vsc-thumbnail", s3Key, ExtraArgs={"ContentType": "image/jpeg"})


