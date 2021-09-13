#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

def upload_graph(imgName):
    bucket = "vsc-graph"
    filePath = "/root/vtuber/vsc/realtime_livedata/img/" + imgName

    s3 = boto3.resource("s3")
    s3.Bucket(bucket).upload_file(Filename=filePath, Key=imgName)

