"""
Utils...

@author FATESAIKOU
"""

# System Imports
import json
import socket

import pprint

def loadFile(filename):
	src = open(filename, 'r')
	content = src.read()
	src.close()

	return content

def getSetting(filename, aim=None):
	settings = json.loads( loadFile(filename) )

	return settings[aim] if ( aim != None and settings.has_key(aim) ) else settings

def getBenchmarkResult(filename):
    benchmark = json.loads(loadFile(filename))
    r_benchmark = []
    for e in benchmark:
      r_benchmark.append(e)

    return r_benchmark

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

def createSockets(worker_hosts):
	socks = {}
	for worker in worker_hosts:
		socks[worker["host"]] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socks[worker["host"]].connect((worker["host"], worker["port"]))

	return socks

def requestMsg(send_msg, wait_msg, sock, recive_size, ttl=10):
	while True:
		sock.send(send_msg)

		msg = sock.recv(recive_size)
		if msg == wait_msg or wait_msg == None:
			break

	return msg

def endTest(worker_hosts, socks, shutdown_server=False):
	for worker in worker_hosts:
		if shutdown_server == True:
			socks[worker["host"]].send('end-server')
		else:
			socks[worker["host"]].send('end')

def getDeviceList(worker_hosts, socks):
	device_list = {}
	for worker in worker_hosts:
		sock = socks[worker["host"]]

		requestMsg('get-device-list', 'Connection-Success', sock, 1024)
		result_size = int( requestMsg('Exec', None, sock, 1024) )
		device_ids = json.loads( requestMsg('Got-Size', None, sock, result_size) )

		device_list[worker["host"]] = device_ids

	return device_list

def getPerformance(banchmark_srcs, device_list, worker_hosts, socks):
	execution_scores = {}
	for worker in worker_hosts:
		sock = socks[worker["host"]]
		test_devices = device_list[worker["host"]]
		execution_scores[worker["host"]] = {}

		for test_device in test_devices:
			test_benchmark_src = banchmark_srcs['cpu' if 'cpu' in test_device else 'gpu']
			test_benchmark_src_size = len(test_benchmark_src)

			requestMsg('get-performance', 'Connection-Success', sock, 1024)
			requestMsg(str(test_benchmark_src_size), 'Got-Size', sock, 1024)
			result_size = int(requestMsg(test_benchmark_src, None, sock, 1024))
			execution_time = float(requestMsg('Got-Size', None, sock, result_size))

			execution_scores[worker["host"]][test_device] = execution_time

	return execution_scores

def getNetCon(net_test_info, worker_hosts, socks):
	""" Net Test Paramater Initialization """
	connect_host = net_test_info["host"]
	multiplier = max(1, 100.0 / net_test_info["datasize"])
	transfer_size = min(100, net_test_info["datasize"])

	""" Iperf Command """
	sh_command = "iperf -c %s -n %d | grep sec | awk '{print $4}'" % (connect_host, transfer_size * 1024 * 1024)

	""" Start Run """
	network_scores = {}
	for worker in worker_hosts:
		sock = socks[worker["host"]]

		requestMsg('get-net-con', 'Connection-Success', sock, 1024)
		requestMsg(sh_command, 'Got-Cmd', sock, 1024)
		result_size = int(requestMsg('Exec', None, sock, 1024))
		transfer_time = float(requestMsg('Got-Size', None, sock, result_size))

		network_scores[worker["host"]] = max(0.000001, transfer_time * multiplier)

	return network_scores

def wrap(worker_hosts, device_list, execution_scores, network_scores):
	benchmark_result = []

	for worker in worker_hosts:
		for device in device_list[worker["host"]]:
			benchmark_result.append({
				"host-name": worker["host"],
				"device-name": device,
				"execution-score": execution_scores[worker["host"]][device],
				"network-score": network_scores[worker["host"]]
			})

	return benchmark_result
