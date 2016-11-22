#!/usr/bin/env python
#argv = Benchmark.py Setting.json Benchmark_result.json

# System Imports
import sys
import json
import time
import Utils

# TensorFlow Inports
import tensorflow as tf

# For Debug
import pprint


""" Env Paramaters Initialization """
benchmark_file = sys.argv[1] if len(sys.argv) > 1 else '../data/Benchmark.py'
setting_file = sys.argv[2] if len(sys.argv) > 2 else '../data/Setting.json'
output_file_name = sys.argv[3] if len(sys.argv) > 3 else '../data/benchmark_result.json'


""" Env Initialization """
worker_hosts = Utils.getSetting(setting_file, "clusters")
benchmark_src = Utils.loadFile(benchmark_file)


""" TensorFlow Env Initialization """
cluster = tf.train.ClusterSpec({"worker": worker_hosts})
device_list = Utils.getDeviceList(worker_hosts)


""" Benchmark """
device_score_list = []

for device in device_list:
    with tf.device(device):
        start = time.time()
        exec(benchmark_src)
        end = time.time()

        device_score_list.append({'name': device, 'exec-time': end - start})


""" Wrapping """
# some wrapping option here


""" Output """
Utils.saveFile(output_file_name, json.dumps(device_score_list))
