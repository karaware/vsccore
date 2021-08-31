#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import schedule
import redis
import main
import operation_redis

# 開始のジョブ
def startJob():
    # 5分毎に実施するジョブ登録
    schedule.every(5).minutes.do(runJob)
    print('startJob：' + str(datetime.datetime.now()))

# 実際に実行したいメイン処理
def runJob():
    print('runJob：' + str(datetime.datetime.now()))
    main.main()

# 終了のジョブ
def endJob():
    print('endJob：' + str(datetime.datetime.now()))
    
    for jobV in schedule.jobs:
        print(str(jobV))
        if 'runJob' in str(jobV):
            # メイン処理のジョブを削除
            schedule.cancel_job(jobV)
            break
    exit()

# 開始するジョブと終了するジョブを定義する
#schedule.every().day.at("14:08").do(startJob)
#schedule.every().day.at("14:09").do(endJob)

scheduledStartTime = operation_redis.get_scheduled_start_time()
dtScheduledStartTime = datetime.datetime.strptime(scheduledStartTime, '%Y/%m/%d %H:%M:%S')
dtScheduledBeforeTenMin = dtScheduledStartTime - datetime.timedelta(minutes=10)

scheduleSetFlug = "false"
endFlag = "false"

while True:
    dtNow = datetime.datetime.now()
    #strDtNow = dtNow.strftime('%Y/%m/%d %H:%M:%S')

    if scheduleSetFlug == "false":
        print("scheduleSetFlug false")
        print(dtScheduledBeforeTenMin)
        print(dtNow)

        if dtScheduledBeforeTenMin < dtNow:
            print("dtScheduledBeforeTenMin < dtNow")
            schedule.every(1).minutes.do(runJob)
            scheduleSetFlug = "true"
        else:
            print("dtScheduledBeforeTenMin > dtNow")

    endFlag = operation_redis.get_end_flag()

    if endFlag == "true":
        dtEndTime = dtScheduledStartTime + datetime.timedelta(minutes=10)
        endTime = dtEndTime.strftime('%H:%M')
        schedule.every().day.at(endTime).do(endJob)


    all_jobs = schedule.get_jobs()
    print(all_jobs)
    print("before run")
    


    schedule.run_pending()
    time.sleep(1)


