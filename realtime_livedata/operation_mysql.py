#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import operation_redis
import log_vsc

def insert_result():
    logger = log_vsc.logger_set()

    conn = mysql.connector.connect(
        host='vsc-mysql.cmuaihicpyco.ap-northeast-1.rds.amazonaws.com',
        port='3306',
        user='admin',
        password='8GsFt6Pd4CTbHdnb',
        #database='vsc'
        database='vscwebdb'
    )
    
    #videoId = "k6KvjFvMeU8"
    #videoTitle = "test2"
    #startTime = "2021/09/08_18:44:00"
    #endTime = "2021/09/08_18:50:00"
    #likeCount= "101"
    #maxViewers = "201"
    #videoUrl = "https://www.youtube.com/watch?v=k6KvjFvMeU8"
    #s3ThumbnailUrl = "https://vsc-thumbnail.s3.ap-northeast-1.amazonaws.com/njiro/20210905_2240_Rbs9w_aKBdg_thumbnail.jpg"
    #s3GraphUrl = "https://vsc-graph.s3.ap-northeast-1.amazonaws.com/njiro/20210905_2248_Rbs9w_aKBdg_liveresult.png"

    videoId = operation_redis.get_current_video_id()
    videoTitle = operation_redis.get_current_title()
    startTime = operation_redis.get_actual_start_time()
    endTime = operation_redis.get_actual_end_time()
    videoUrl = "https://www.youtube.com/watch?v=" + videoId
    likeCount = operation_redis.get_current_like_count()
    maxViewers = operation_redis.get_max_viewers()
    s3ThumbnailUrl = "https://vsc-thumbnail.s3.ap-northeast-1.amazonaws.com/njiro/" + operation_redis.get_thumbnail_img_name()
    s3GraphUrl = "https://vsc-graph.s3.ap-northeast-1.amazonaws.com/njiro/" + operation_redis.get_graph_img_name()


    cur = conn.cursor()

    #sql = "INSERT INTO njiro_result ( \
    sql = "INSERT INTO vscwebnjiro_resultmodel ( \
    videoId, \
    videoTitle, \
    startTime, \
    endTime, \
    likeCount, \
    maxViewers, \
    videoUrl, \
    s3ThumbnailUrl, \
    s3GraphUrl \
    ) VALUES (" \
    + "'" + videoId + "'," \
    + "'" + videoTitle + "'," \
    + "'" + startTime + "'," \
    + "'" + endTime + "'," \
    + likeCount + "," \
    + maxViewers + "," \
    + "'" + videoUrl + "'," \
    + "'" + s3ThumbnailUrl + "'," \
    + "'" + s3GraphUrl + "')"

    print(sql)

    print("-----------")

    cur.execute(sql)

    #cur.execute("INSERT INTO vsc_result VALUES (" + "'" + videoId + "'," + "'" +videoTitle + "'," + "'" +startTime + "'," + "'" +endTime + "," + likeCount + "," + maxViewers + "'," + "'" +videoUrl + "'," + "'" +s3ThumbnailUrl + "'," + "'" +s3GraphUrl + "');" + ")

    #cur.execute("SELECT * FROM njiro_result")
    cur.execute("SELECT * FROM vscwebnjiro_resultmodel")

    rows = cur.fetchall()

    for row in rows:
        print(row)
        logger.log(10, row)

    conn.commit()
    
    cur.close()
    conn.close()



#insert_result()

