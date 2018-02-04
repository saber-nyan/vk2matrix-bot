# -*- coding: utf-8 -*-
"""
Bot configuration file.
It takes settings from environment variables.
"""
import os
import sys
import traceback

# var = os.getenv('key', default)

# IMPORTANT: each variable has a MATRIX_ prefix to avoid conflicts.

p = 'MATRIX_'

# noinspection PyBroadException
try:
    USERNAME = os.environ[p + 'USERNAME']  # Matrix bot username
    PASSWORD = os.environ[p + 'PASSWORD']  # Matrix bot password
    VK_LOGIN = os.environ[p + 'VK_LOGIN']  # vk.com login (phone number is preferred)
    VK_PASSWORD = os.environ[p + 'VK_PASSWORD']  # vk.com password
except:
    print("Please set necessary ENV variables!\n"
          "Read more in config.py or README.md.\n\n"
          "Details:\n{}".format(traceback.format_exc()), file=sys.stderr)
    sys.exit(1)

# Matrix server URL. Auth at https://vector.im?
SERVER = os.getenv(p + 'SERVER', "https://matrix.org")


logfmt_default = '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: %(message)s'
LOG_FORMAT = os.getenv(p + 'LOG_FORMAT', logfmt_default)

# Available levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET
LOG_LEVEL = os.getenv(p + 'LOG_LEVEL', 'INFO')

