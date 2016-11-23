#!/usr/bin/env python
#argv = Benchmark.py Setting.json Benchmark_result.json

# System Imports
import sys
import json
import Utils


# For Debug
import pprint


""" Env Paramaters Initialization """
cpu_benchmark_file = sys.argv[1] if len(sys.argv) > 1 else '../data/Cpu-Benchmark.py'
gpu_benchmark_file = sys.argv[2] if len(sys.argv) > 2 else '../data/Gpu-Benchmark.py'
setting_file = sys.argv[3] if len(sys.argv) > 3 else '../data/Setting.json'
output_file_name = sys.argv[4] if len(sys.argv) > 4 else '../data/benchmark_result.json'


""" Env Initialization """
worker_hosts = Utils.getSetting(setting_file, "clusters")
net_test_info = Utils.getSetting(setting_file, "net-test-info")
benchmark_srcs = {
    "cpu": Utils.loadFile(cpu_benchmark_file),
    "gpu": Utils.loadFile(gpu_benchmark_file)
}
worker_hosts = [{"host": "master", "port": 22222}]


""" Network Connection Initialization """
socks = Utils.createSockets(worker_hosts)


""" Get Device List """
device_list = Utils.getDeviceList(worker_hosts, socks)
pprint.pprint(device_list)


""" Performance Benchmark """
execution_scores = Utils.getPerformance(benchmark_srcs, device_list, worker_hosts, socks)
pprint.pprint(execution_scores)


""" Network Benchmark """
network_scores = Utils.getNetCon(net_test_info, worker_hosts, socks)
pprint.pprint(network_scores)


""" Wrapping Result """
benchmark_result = {}


""" Output """
Utils.saveFile(output_file_name, json.dumps(benchmark_result))
pprint.pprint(benchmark_result)

""" Ending """
Utils.endTest(worker_hosts, socks)
