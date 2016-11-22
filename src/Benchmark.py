#!/usr/bin/env python
#argv = Setting.json

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
setting_file = sys.argv[1]
benchmark_file = sys.argv[2]
output_file_name = sys.argv[3]


""" Env Initialization """
worker_hosts = Utils.getSetting(setting_file, "clusters")
benchmark_src = Utils.loadFile(benchmark_file)


""" TensorFlow Env Initialization """
cluster = tf.train.ClusterSpec({"worker": worker_hosts})
device_list = Utils.getDeivceList(worker_hosts)


""" Benchmark """
device_score_list = []

for device in device_list:
    with tf.device(device):
        start = time.time()
        exec(benchmark_src)
        end = time.time()

        device_score_list.append({'name': device, 'exec-time': end - start})

""" Wrapping """


""" Output """
Utils.saveFile(output_file_name, json.dump(device_score_list))
