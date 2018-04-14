#!/usr/bin/ python3
# -*-coding:utf-8-*-
import logging

from . import api
from ihome import models


@api.route("/index")
def index():
    logging.debug("调试信息")
    logging.info("详情信息")
    logging.warning("警告信息")
    logging.error("错误信息")

    return "index"