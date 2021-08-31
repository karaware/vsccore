#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import redis
import numpy as np
import matplotlib as mpl
mpl.use('Agg') # AGG(Anti-Grain Geometry engine)
import matplotlib.pyplot as plt
import datetime
import tweet
import logging

def make_graph():
    # ログ設定
    logger = logging.getLogger('LoggingTest')
    logger.setLevel(10)
    fh = logging.FileHandler('/home/pi/vtuber/tomeru/realtime_livedata/test.log')
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
    fh.setFormatter(formatter)

    logger.log(10, 'live_result 1')

    r = redis.Redis(host='localhost', port=6379, db=3)

    timeLists = r.lrange("timeRecord", 0, -1)
    #print(timeLists)
    strTimeLists = []
    for byteTime in timeLists:
        strTimeLists.append(byteTime.decode())
    print(strTimeLists)

    viewerLists = r.lrange("viewersRecord", 0, -1)
    #print(viewerLists)
    intViewerLists = []
    for byteViewer in viewerLists:
        intViewerLists.append(int(byteViewer.decode()))
    print(intViewerLists)

    logger.log(10, 'live_result 2')

    left = np.array(strTimeLists)
    height = np.array(intViewerLists)

    plt.plot(left, height, marker="o")

    plt.xticks(rotation=90)

    plt.xlabel('timestamp')
    plt.ylabel('viewer')
    plt.grid(color='b', linestyle=':', linewidth=0.3)

    dtNow = datetime.datetime.now()
    strDtNow = dtNow.strftime("%Y%m%d_%H%M")
    imgPath = "/home/pi/vtuber/tomeru/realtime_livedata/img/" + strDtNow + "_liveresult.png"

    logger.log(10, 'live_result 3')

    #plt.savefig('./img/ret.png')
    plt.savefig(imgPath)

    logger.log(10, 'live_result 4')

    tweet.result_tweet(imgPath)


#make_graph()



