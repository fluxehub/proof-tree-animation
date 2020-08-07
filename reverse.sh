#!/bin/bash

# Optional script to reverse video

mkdir media/output

for video in media/videos/*/1440p60/*.mp4
do
    ffmpeg -i $video -filter_complex "[0:v]reverse,fifo[r];[0:v][r][0:v] concat=n=3:v=1 [v]" -map "[v]" media/output/$(basename "$video")
done