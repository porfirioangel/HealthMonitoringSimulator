#!/usr/bin/env python
# coding=utf-8

'''
Este script es un ejemplo de cómo se puede programar una tarea para ser
ejecutada en una hora específica
'''

from datetime import datetime
from threading import Timer

x = datetime.today()
y = x.replace(day=x.day, hour=0, minute=0, second=5, microsecond=0)
delta_t = y - x

secs = delta_t.seconds + 1


def hello_world():
    print "hello world"


t = Timer(secs, hello_world)
t.start()
