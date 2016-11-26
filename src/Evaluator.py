# System Imports
import math
import json
import re

# Our Library
import Utils

# For Debug
import pprint

""" Find the optimization setting """
def getOptimization(weight_file, benchmark_file, data):
  opt_setting = []

  """ Env Initialization """
  """                    """
  """ weight_list(Object)"""
  """ each element       """
  """ {                  """
  """   keyword: grade   """
  """ }                  """
  weight_list = Utils.getWeightList(weight_file)
  benchmark = Utils.getBenchmarkResult(benchmark_file)

  data.node = countWeight(weight_list, data.node)

  """ Example Output """
  opt_setting.append({
    'node_id': 0,
    'benchmark_id': 0
  })

  return opt_setting

""" Example Count Weight """
def countWeight(weight_list, node):
  for keyword, grade in weight_list.iteritems():
    for idx in node:
      if(re.search(keyword, node[idx]['content'])):
        node[idx]['grade'] += grade

  return node

