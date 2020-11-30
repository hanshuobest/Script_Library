#!/bin/sh
for i in *.wav;
do
ffmpeg -i "$i" -f mp3 "${i}.mp3";
rename .wav.mp3 .mp3 *.wav.mp3;
done
# find *.wav|xargs rm -rf #如果需要保留原.wav 可以注释掉这行 
