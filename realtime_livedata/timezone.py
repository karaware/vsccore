#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from pytz import timezone

def utc_to_jst(utcTime):

    dte = datetime.datetime.strptime(utcTime, '%Y-%m-%dT%H:%M:%SZ')

    jstDte = dte + datetime.timedelta(hours=9)

    jstStartTime = jstDte.strftime('%Y/%m/%d_%H:%M:%S')

    return jstStartTime


