#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from pytz import timezone

def utc_to_jst(utcTime):

    dte = datetime.datetime.strptime(utcTime, '%Y-%m-%dT%H:%M:%SZ')

    jstDte = dte + datetime.timedelta(hours=9)

    jstStartTime = jstDte.strftime('%Y/%m/%d_%H:%M:%S')

    return jstStartTime

input = "2021-08-08T11:00:00Z"
#print("[UTC] " + input)
#print("[JST] " + utc_to_jst(input))

