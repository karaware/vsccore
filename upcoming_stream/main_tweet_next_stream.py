#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operation_redis
import tweet

nextStream = operation_redis.get_next_stream()
tweet.tweet_next_steam(nextStream)

