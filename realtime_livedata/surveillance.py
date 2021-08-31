#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import schedule
import redis
import main
import operation_redis
import logging

# ログ設定
logger = logging.getLogger('LoggingTest')
logger.setLevel(10)
fh = logging.FileHandler('/home/pi/vtuber/tomeru/realtime_livedata/test.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
logger.log(10, 'surveillance 0')


dtNow = datetime.datetime.now()
scheduledStartTime = operation_redis.get_scheduled_start_time()
dtScheduledStartTime = datetime.datetime.strptime(scheduledStartTime, '%Y/%m/%d %H:%M:%S')
dtScheduledBeforeTenMin = dtScheduledStartTime - datetime.timedelta(minutes=10)

endFlag = operation_redis.get_end_flag()

if dtScheduledBeforeTenMin < dtNow and endFlag == "false":
    print("dtScheduledBeforeTenMin < dtNow")
    logger.log(10, 'surveillance 1 dtScheduledBeforeTenMin < dtNow')
    main.main()
elif dtScheduledBeforeTenMin > dtNow:
    print("stream is not start")
elif endFlag == "true":
    print("stream was finished")


