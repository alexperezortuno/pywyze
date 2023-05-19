#!/bin/bash
VIDSOURCE="rtsp://aportuno:97531@192.168.1.63/live"
AUDIO_OPTS="-c:a aac -b:a 40000 -ac 1"
VIDEO_OPTS="-c:v copy -bufsize 1M -pix_fmt rgb24 -s 360x240 -c:v libx264 -b:v 2M -maxrate 2M -flags -global_header"
OUTPUT_HLS="-hls_time 10 -hls_list_size 5 -hls_wrap 50 -start_number 1"
ffmpeg -i "$VIDSOURCE" -y $AUDIO_OPTS $VIDEO_OPTS $OUTPUT_HLS /media/hdca/Workspace/Projects/Python/pywyze/media/playlist.m3u8
