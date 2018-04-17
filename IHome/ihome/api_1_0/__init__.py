#!/usr/bin/ python3
# -*-coding:utf-8-*-
from flask import Blueprint


api = Blueprint("api_1_0", __name__)

from . import verify
from . import passport
from . import profile