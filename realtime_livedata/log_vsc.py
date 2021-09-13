#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

def logger_set():
    logger = logging.getLogger('LoggingTest')
    logger.setLevel(10)
    fh = logging.FileHandler('/root/vtuber/vsc/realtime_livedata/realtime_livedata.log')
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    logger.log(10, 'surveillance 0')

    return logger

