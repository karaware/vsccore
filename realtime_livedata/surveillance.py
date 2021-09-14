#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import schedule
import redis
import main
import operation_redis
import log_vsc

logger = log_vsc.logger_set()

dtNow = datetime.datetime.now()
scheduledStartTime = operation_redis.get_scheduled_start_time()

try:
    dtScheduledStartTime = datetime.datetime.strptime(scheduledStartTime, '%Y/%m/%d %H:%M:%S')
except:
    print('next_stream not found')
    logger.log(10, 'next_stream not found')
    exit()

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


