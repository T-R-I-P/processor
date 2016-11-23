"""
Utils...

@author FATESAIKOU
"""

# System Imports
import json

# TensorFlow Imports
from tensorflow.python.client import device_lib
import tensorflow as tf

def loadFile(filename):
    src = open(filename, 'r')
    content = src.read()
    src.close()

    return content

def getSetting(filename, aim=None):
    settings = json.loads( loadFile(filename) )

    return settings[aim] if ( aim != None and settings.has_key(aim) ) else settings

def getDeviceList(worker_hosts):
    device_list = []

    for i in xrange(len(worker_hosts)):
        now_worker_name = 'job:worker/task:%d' % (i)
        with tf.device(now_worker_name):
            device_ids = [ device.name for device in device_lib.list_local_devices()]
            device_list.extend([ (now_worker_name + device_id) for device_id in device_ids ])

    return device_list

def getBenchmarkResult(filename):
  benchmark = json.loads(loadFile(filename))

  return benchmark

def getWeightList(filename):
  weight_list = json.loads(loadFile(filename))

  """ Convert to int """
  for idx in weight_list:
    weight_list[idx] = int(weight_list[idx])

  return weight_list

def saveFile(filename, content):
    src = open(filename, 'w')
    src.write(content)
    src.close()
