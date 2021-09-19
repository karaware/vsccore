#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import redis
import numpy as np
import matplotlib as mpl
mpl.use('Agg') # AGG(Anti-Grain Geometry engine)
import matplotlib.pyplot as plt
import datetime
from datetime import datetime as dt
import tweet
import log_vsc
import operation_s3
import os
import operation_redis

def make_graph():

    logger = log_vsc.logger_set()

    logger.log(10, 'live_result 1')

    strTimeLists = operation_redis.get_time_record()
    dateTimeLists = [dt.strptime(d, '%H:%M') for d in strTimeLists]

    intViewerLists = operation_redis.get_viewers_record()

    logger.log(10, 'live_result 2')

    #left = np.array(strTimeLists)
    left = np.array(dateTimeLists)
    height = np.array(intViewerLists)

    logger.log(10, 'live_result 3')

    plt.plot(left, height)

    plt.xticks(rotation=90)

    plt.xlabel('timestamp')
    plt.ylabel('viewer')
    plt.grid(color='b', linestyle=':', linewidth=0.3)

    logger.log(10, 'live_result 4')

    dtNow = datetime.datetime.now()
    strDtNow = dtNow.strftime("%Y%m%d_%H%M")

    videoId = operation_redis.get_current_video_id()

    imgName =  strDtNow + "_" + videoId + "_graph.png"

    thumbnailImgName =  strDtNow + "_" + videoId + "_thumbnail.jpg"

    imgDir = "/home/vsc/vsccore/tomeru/realtime_livedata/img/"

    imgPath = imgDir + imgName

    logger.log(10, 'live_result 5')

    logger.log(10, 'imgPath' + imgPath)

    logger.log(10, 'live_result 6')

    plt.savefig(imgPath)

    logger.log(10, 'live_result 7')

    tweet.result_tweet(imgPath)

    logger.log(10, 'live_result 8')

    operation_s3.upload_graph(imgName)

    #operation_s3.upload_thumbnail(thumbnailImgName)

    logger.log(10, 'live_result 9')

    #os.remove(imgPath)

#make_graph()



