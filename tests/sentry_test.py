# -*- coding:utf-8 -*-

#测试文件，测试发送的错误信息到日志监控

DSN = 'https://503fe4bb9096453b8fc0e20fd469e5eb:3a4a1a20aa944f588d61e1504f1aa1a1@sentry.io/265375'

from raven import Client

client = Client(DSN)

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()