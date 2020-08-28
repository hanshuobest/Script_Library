#! /usr/bin/bash
while true ; do rsync -vauP /Users/han/Deeplearning/darknet/*  --exclude=".*" --exclude="data/" --exclude="cfg"    han@10.1.57.16:~/Desktop/darknet; sleep 10; done
