#!/usr/bin/env python
"""
Get Device List

@author FATESAIKOU
"""

import json

from tensorflow.python.client import device_lib

print json.dumps( [ device.name for device in device_lib.list_local_devices() ] )
