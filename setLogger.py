#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# 创建日期: 2017/3/6
__author__ = 'kylinpoet'

import logging
import os
import sys

def setLogger(logfile = sys.argv[0] + '.log'):
    # 创建一个logger,可以考虑如何将它封装
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(filename=os.path.join(os.getcwd(), logfile),mode='a')
    fh.setLevel(logging.DEBUG)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S %A,')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    # 记录一条日志
    # logger.info('hello world, i\'m log helper in python, may i help you')
    return logger

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S %A,',
#                     filename='get_wz_weather.log',
#                     filemode='a')
if __name__ == '__main__':
    mylogger = setLogger()
    try:
        a = 1/0
    except Exception as e:
        mylogger.exception(e)