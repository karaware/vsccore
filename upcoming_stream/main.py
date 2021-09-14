#!/usr/bin/env python
# -*- coding: utf-8 -*-

import upcoming_stream
import next_stream
import operation_redis
import log_vsc

logger = log_vsc.logger_set()

currentLiveStatus = operation_redis.get_current_live_status()

if currentLiveStatus == "none":
    print('currentLiveStatus is none')
    logger.log(10, 'currentLiveStatus is none')

    upcoming_stream.set_upcoming_stream()
    next_stream.set_next_stream()
else:
    print('currentLiveStatus is live')
    logger.log(10, 'currentLiveStatus is live')

