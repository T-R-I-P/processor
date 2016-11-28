# System Imports
import math
import json
import re

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
  """ Example Output """
  """ node_id => Which node  """
  """ host_id => Which Host  """
  """ benchmark_id => Which Host and Which Device """

  opt_setting = []
  opt_setting.append({
    'node_id': 0,
    'host_id': 0,
    'benchmark_id': 0
  })

  return opt_setting

