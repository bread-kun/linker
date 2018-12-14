#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import time
from functools import wraps
import logging

logging.basicConfig(filename='game_time.log', level=logging.INFO)
# derector for count how many time function spend
# @type		derector
def clocker(func):
	"""docstring for Clocker"""
	@wraps(func)
	def _call_(*args, **kwargs):
		_res = None
		logging.info("===> function \'{}\' start run....".format(func.__name__))
		_start = time.clock()
		_res = func(*args,**kwargs)
		_end = time.clock() - _start
		logging.info("===> function \'{}\' use time: {:.8f} second".format(func.__name__, _end))
		return _res
	return _call_