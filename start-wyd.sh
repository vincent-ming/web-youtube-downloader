#!/bin/bash

pid=$(ps aux | grep "web-youtube-downloader" | grep -v grep | awk '{print $2}')

if [ -n "$pid" ]; then
        echo "kill web-youtube-downloader pid $pid"
        kill -9 $pid;
fi

nohup uvicorn main:app --app-dir ./app --host 0.0.0.0 --port 9000 > /dev/null 2>&1 &
echo 'start wyd success'