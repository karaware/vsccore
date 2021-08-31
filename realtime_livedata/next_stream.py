#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operation_redis

def set_next_stream():
    nextStream = operation_redis.get_next_stream()

    operation_redis.flush_db_2()

    operation_redis.set_next_stream(nextStream)

#set_next_stream()
