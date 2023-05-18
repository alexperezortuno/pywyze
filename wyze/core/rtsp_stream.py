#!/usr/src/env python
# -*- coding: utf-8 -*-
import sys

import cv2
import imutils
from imutils.video import VideoStream


class VideoCameras:
    def get_cam(self):
        rtsp_url: str = 'rtsp://aportuno:97531@192.168.1.63/live'
        video_stream = VideoStream(src=rtsp_url)


        try:
            while True:
                frame = video_stream.read()
                if frame is None:
                    print("No frame")
                    continue

                frame = imutils.resize(frame, width=400)
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
        except KeyboardInterrupt:
            sys.exit(0)
