#!/usr/src/env python
# -*- coding: utf-8 -*-
import argparse
from typing import Dict

from wyze.core.commons import log_lvl, log_str
from wyze.core.logger import get_logger
from wyze.core.wyze import Wyze


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="ZeroMQ workers",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        subparser = parser.add_subparsers(title='Script select', dest='script_type')
        parser.version = '0.0.0'
        parser.add_argument("-v", "--version", action="version")
        parser.add_argument("-d", "--devices", type=bool, default=False)
        parser.add_argument("--log_level", type=str, default=log_lvl)
        parser.add_argument("--log_format", type=str, default=log_str)
        params: Dict = vars(parser.parse_args())

        logger = get_logger(params['log_level'], params['log_format'], __name__)

        w = Wyze(params)
        w.start()
    except KeyboardInterrupt:
        print("Program stopped by user.")
    except Exception as e:
        print(e)
        print("Program stopped due to an error.")
