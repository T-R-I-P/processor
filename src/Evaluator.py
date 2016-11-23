# System Imports
import math
import json
import re
import time

# Our Library
import Utils

# For Debug
import pprint

""" Find the optimization setting """
def getOptimization(setting_file, weight_file, benchmark_file, meta):
  print 'Find the optimization setting'

  """ Env Initialization """
  exec_code = ''
  node_code = ''
  start = 0
  end = 0
  weight_list = Utils.getWeightList(weight_file)
#  worker_hosts = Utils.getSetting(setting_file, "clusters")
  worker_hosts = Utils.getSetting(setting_file, "localhost")
  benchmark = Utils.getBenchmarkResult(benchmark_file)

  """ TensorFlow Env Initialization """
  device_list = Utils.getDeviceList(worker_hosts)

  """ Count grade """
  meta['node']['ele'] =  countWeight(meta['node']['ele'], weight_list)
  meta['node']['ele'] = countMatmul(meta['node']['ele'], meta['variable']['matmul'], meta['variable']['ele'])

  exec_code = meta['header'] + node_code + meta['execute']


  start = time.time()
  #exec(exec_code)
  end = time.time()

def countWeight(node, weight_list):
  for idx, ele in enumerate(node):
    """ Count keyword grade """
    for weight_element in weight_list:
      if(re.search(weight_element, ele['content'])):
        ele['grade'] += weight_list[weight_element]

    node[idx] = ele

  return node

def countMatmul(node, src_matmul, src_ele):
  first_var = ''
  second_var = ''
  first_val = 0
  second_val = 0
  node_id = 0
  grade = 0

  for e_matmul in src_matmul:
    node_id = e_matmul['node_id']
    first_var = e_matmul['value'][0]
    second_var = e_matmul['value'][1]

    """ Search matmul elements, and get the grade of the variable """
    for e_ele in src_ele:
      if(e_ele['name'] == first_var):
        if(e_ele['value'][0] == 'None'):
          first_val = 1# Edit None Value here
        else:
          first_val = int(e_ele['value'][0])
      elif(e_ele['name'] == second_var):
        second_val = int(e_ele['value'][1])

    """ Grade by our rules """
    grade = math.sqrt(first_val * second_val)
    node[node_id]['grade'] += grade

  return node


