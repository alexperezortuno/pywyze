#!/usr/src/env python
# -*- coding: utf-8 -*-
import os
from typing import Dict, Any
from wyze_sdk import Client

from wyze.core.exceptions import ClientException
from wyze.core.logger import get_logger
from wyze.core.rtsp_stream import VideoCameras


class Wyze:
    access_token: str
    refresh_token: str
    params: Dict
    logger: Any
    log_lvl: str
    log_str: str

    def __init__(self, params: Dict):
        self.access_token = ''
        self.refresh_token = ''
        self.params = params
        self.log_lvl = params['log_level']
        self.log_str = params['log_format']
        self.logger = get_logger(self.log_lvl.upper(), self.log_str, __name__)

    @classmethod
    def get_credentials(cls):
        response: Any
        connect = Client().login(
            email=os.environ["WYZE_EMAIL"],
            password=os.environ["WYZE_PASSWORD"],
            totp_key=os.environ["WYZE_MFA_CODE"])
        response = connect.data

        return response

    def get_client(self) -> Client or None:
        try:
            client = Client(token=self.access_token)
            return client
        except Exception as ex:
            self.logger.debug(ex)
            return None

    def get_devices(self) -> list:
        client = self.get_client()
        if client is None:
            raise ClientException()

        return client.devices_list()

    def start(self):
        if self.access_token == '':
            get_data = self.get_credentials()
            self.access_token = get_data['access_token']
            self.refresh_token = get_data['access_token']

        if self.params['devices']:
            devices: list = self.get_devices()
            if len(devices) == 0:
                self.logger.info('No have devices')
                return None

            for device in devices:
                self.logger.info(f'MAC: {device.mac}')
                self.logger.info(f'nickname: {device.nickname}')
                self.logger.info(f'is_online: {device.is_online}')
                self.logger.info(f'IP: {device.ip}')
                self.logger.info(f'product_model: {device.product.model}')

        video_stream = VideoCameras()
        video_stream.get_cam()
