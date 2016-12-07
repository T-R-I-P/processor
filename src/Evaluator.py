# System Imports
import math
import json
import re
from operator import itemgetter, attrgetter, methodcaller

# Our Library
import Utils

# For Debug
import pprint

""" Find the optimization setting """
def getOptimization(weight_file, setting_file, benchmark_file, data):
  """ Env Initialization """
  """                    """
  """ weight_list(Object)"""
  """ each element       """
  """ {                  """
  """   keyword: grade   """
  """ }                  """
  weight_list = Utils.getWeightList(weight_file)

  """ benchmark(array)             """
  """                              """
  """ index is benchmark_id        """
  """ each element                 """
  """ {                            """
  """   device-name: /cpu:0,       """
  """   host-name: master,         """
  """   execution-score: 6.844493, """
  """   network-score: 1e-06       """
  """ }                            """
  benchmark = Utils.getBenchmarkResult(setting_file, benchmark_file)

  """ Node Class                         """
  """ ---------------------------------- """
  """ node (array)                       """
  """                                    """
  """ index is node_id                   """
  """ Each Element                       """
  """ {                                  """
  """   'content': [source string]       """
  """   'lines': [source lines]          """
  """   'device_id': [device_id]         """
  """   'grade': [grade]                 """
  """ }                                  """
  """ ---------------------------------- """
  """ variable (array)                   """
  """                                    """
  """ Each Element                       """
  """ {                                  """
  """   'node_id': [node_id] Belong which node """
  """   'name': [name] Variable name           """
  """   'type': matmul, placeholder ...  """
  """   'value': [None, 100], or [x, y_] """
  """ }                                  """
  """ ---------------------------------- """
  """ matmul (array)                     """
  """                                    """
  """ Each Element                       """
  """ {                                  """
  """   'node_id': [node_id] Belong which node """
  """   'variable_id': [variable_id]     """
  """   'grade': -1 means not count      """
  """   'value': [None, 100], or [x, y_] """
  """ }                                  """


  data.node = countWeight(weight_list, data.node)
  data.node = countMatmul(data)
  opt_setting = pairAlgorithm(data, benchmark)

  return opt_setting

""" Example Count Weight """
def countWeight(weight_list, node):
  for keyword, grade in weight_list.iteritems():
    for idx, e in enumerate(node):
      if(re.search(keyword, e['content'])):
        node[idx]['grade'] += grade

  return node

""" Example Count Matmul """
def countMatmul(data):
  """ You get a array for all variable, """
  """ by this method getMatmul([matmul_id], [empty array])"""
  """                   """
  """ If matmul => X, Y """
  """ X = ....(None, 8) """
  """ Y = ....(8, 200)  """
  """ The return is ['None', '8', '8', '200'] """
  for idx, e in enumerate(data.matmul):
    node_id = data.matmul[idx]['node_id']
    r_array = data.getMatmul(idx, [])

    first = r_array[0]
    last = int(r_array[-1])
    """ Define None value """
    if(first == 'None'):
      first = 1
    else:
      fist = int(first)
    data.node[node_id]['grade'] += (first * last)

  return data.node

""" Example for pair each other """
def pairAlgorithm(data, benchmark):
  device = []
  """ if(has gpu) delete cpu """
  for idx, host in enumerate(benchmark['group_by_host']):
    if(len(host['gpu'])!=0):
      for e in host['gpu']:
        device.append(e)
    elif(len(host['cpu'])!=0):
      for e in host['cpu']:
        device.append(e)

  """ Add All """
  total_network_score = 0
  total_execution_score = 0
  total_benchmark_score = 0
  total_node_grade = 0
  for idx, e in enumerate(device):
    total_execution_score += e['execution-score']
    total_network_score += 1/e['network-score']

  for idx, e in enumerate(data.node):
    total_node_grade += e['grade']

  """ Count the %  """
  """ Count Benchmark """
  for idx, e in enumerate(device):
    network_score = (1/e['network-score'])/total_network_score
    execution_score = e['execution-score']/total_execution_score
    device[idx]['benchmark_score'] = (network_score) + (execution_score)
    total_benchmark_score += device[idx]['benchmark_score']
  for idx, e in enumerate(device):
    device[idx]['benchmark_score'] = e['benchmark_score']/total_benchmark_score

  """ Count node grade """
  for idx, e in enumerate(data.node):
    data.node[idx]['grade'] = 1.0*e['grade']/total_node_grade

  """ Sort the device, and node array """
  device = sorted(device, key=itemgetter('benchmark_score'), reverse=True)
  data.node = sorted(data.node, key=itemgetter('grade'), reverse=True)

  """ Example Output """
  """ node_id => Which node  """
  """ host_id => Which Host  """
  """ benchmark_id => Which Host and Which Device """
  opt_setting = []
  """
  Example
  opt_setting.append({
    'node_id': 0,
    'host_id': 0,
    'benchmark_id': 0
  })
  """

  if(len(device) >= len(data.node)):
    for idx, e in enumerate(data.node):
      opt_setting.append({
        'node_id': e['node_id'],
        'host_id': device[idx]['host_id'],
        'benchmark_id': device[idx]['benchmark_id']
      })
  else:
    len_device = len(device)
    idx_device = 0
    for idx, e in enumerate(data.node):
      if(device[idx_device]['benchmark_score'] >= e['grade']):
        device[idx_device]['benchmark_score'] -= e['grade']
        opt_setting.append({
          'node_id': e['node_id'],
          'host_id': device[idx_device]['host_id'],
          'benchmark_id': device[idx_device]['benchmark_id']
        })
      elif(((idx_device+1) == len_device) or (device[idx_device]['benchmark_score'] < device[idx_device+1]['benchmark_score'])):
        """ Final, or less than the next element, resort """
        device = sorted(device, key=itemgetter('benchmark_score'), reverse=True)
        idx_device = 0
        if(device[idx_device]['benchmark_score'] >= e['grade']):
          device[idx_device]['benchmark_score'] -= e['grade']
          opt_setting.append({
            'node_id': e['node_id'],
            'host_id': device[idx_device]['host_id'],
            'benchmark_id': device[idx_device]['benchmark_id']
          })
        else:
          device[idx_device]['benchmark_score'] = 0
          opt_setting.append({
            'node_id': e['node_id'],
            'host_id': device[idx_device]['host_id'],
            'benchmark_id': device[idx_device]['benchmark_id']
          })
          idx_device += 1
      elif(device[idx_device]['benchmark_score'] >= device[idx_device+1]['benchmark_score']):
        device[idx_device]['benchmark_score'] = 0
        opt_setting.append({
          'node_id': e['node_id'],
          'host_id': device[idx_device]['host_id'],
          'benchmark_id': device[idx_device]['benchmark_id']
        })
        idx_device += 1

  pprint.pprint(opt_setting)
  return opt_setting

