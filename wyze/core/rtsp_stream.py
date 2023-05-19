#!/usr/src/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
from datetime import date
from typing import Dict, Any

import cv2
import imutils
from imutils.video import VideoStream

from wyze.core.logger import get_logger


class VideoCameras:
    logger: Any

    def __init__(self, config: Dict = None):
        self.config = config
        self.logger = get_logger(config['log_level'].upper(), config['log_format'], __name__)

    def get_cam(self):
        rtsp_url: str = 'rtsp://aportuno:97531@192.168.1.63/live'
        # video_capture = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        # stream = cv2.VideoCapture(rtsp_url)

        cap = cv2.VideoCapture(rtsp_url)

        try:
            # Crear objeto de captura de video
            fps = cap.get(cv2.CAP_PROP_FPS)
            buffer_size = int(fps * 30)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

            # Establecer la resolución
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

            bitrate = (360 * 240 * fps * 0.5)

            # Establecer la tasa de bits
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
            cap.set(cv2.CAP_PROP_BITRATE, bitrate)

            # Verificar si la cámara está conectada
            if not cap.isOpened():
                print("No se pudo conectar a la cámara")
                exit()

            # Mostrar el video en vivo
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("No se pudo recibir el marco de video")
                    break
                if frame is None:
                    print("No frame")
                    time.sleep(2.0)
                    continue
                height, width, layers = frame.shape
                frame = cv2.resize(frame, (width // 2, height // 2))
                cv2.imshow("Video en vivo", frame)

                # Salir si se presiona la tecla 'q'
                if cv2.waitKey(1) == ord('q'):
                    break
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as ex:
            print(ex)
        finally:
            if cv2 is not None:
                cv2.destroyAllWindows()
            cap.release()

    def get_cam2(self):
        rtsp_url: str = 'rtsp://aportuno:97531@192.168.1.63/live'
        video_stream = VideoStream(src=rtsp_url, resolution=(360, 240)).start()
        try:
            while True:
                frame = video_stream.read()
                if frame is None:
                    print("No frame")
                    time.sleep(2.0)
                    continue
                frame = imutils.resize(frame, width=360)
                cv2.imshow("Frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as ex:
            print(ex)

    def start_cam(self, params: Dict):
        try:
            abs_path: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            rtsp_url: str = f"rtsp://aportuno:97531@{params['ip']}/live"

            if not os.path.exists(f'{abs_path}/media/{date.today().strftime("%Y-%m-%d")}'):
                os.makedirs(f'{abs_path}/media/{date.today().strftime("%Y-%m-%d")}')
                self.logger.debug(f'Directory created "media/{date.today().strftime("%Y-%m-%d")}"')

            output_path = f"{abs_path}/media/{date.today().strftime('%Y-%m-%d')}/{params['name']}.m3u8".replace(' ', '_')

            ffmpeg_cmd = ['ffmpeg',
                          '-i',
                          rtsp_url,
                          '-y',
                          '-c:a',
                          'aac',
                          '-b:a',
                          '40000',
                          '-ac',
                          '1',
                          '-c:v',
                          'copy',
                          '-bufsize',
                          '1M',
                          '-pix_fmt',
                          'rgb24',
                          '-s',
                          '360x240',
                          '-c:v',
                          'libx264',
                          '-b:v',
                          '2M',
                          '-maxrate',
                          '2M',
                          '-hls_time',
                          '5',
                          '-hls_list_size',
                          '3',
                          '-hls_wrap',
                          '50',
                          '-start_number',
                          '1',
                          output_path
                          ]
            self.logger.debug(' '.join(ffmpeg_cmd))
            ffmpeg_cmd = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = ffmpeg_cmd.communicate()
            self.logger.debug(out.decode())
            self.logger.debug(err.decode())
            # time.sleep(10)
            # recorder.stdin.write('q'.encode("GBK"))  # Simulate user pressing q key
            # recorder.communicate()
            # recorder.wait()
            # print(result.stdout.read())
        except Exception as ex:
            print(ex)
        finally:
            pass
