# System Imports
import math
import json
import re

# Our Library
import Utils

# For Debug
import pprint

""" Find the optimization setting """
def getOptimization(setting_file, weight_file, benchmark_file, meta):
  print 'Find the optimization setting'

  weight_list = getWeightList(weight_file)

  meta['node'] =  countWeight(meta['node'], weight_list)
  meta['node'] = countMatmul(meta['node'], meta['variable']['matmul'], meta['variable']['ele'])

#  pprint.pprint(meta['node'])


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

    """ Search matmul elements, and get the grade """
    for e_ele in src_ele:
      if(e_ele['name'] == first_var):
        if(e_ele['value'][0] == 'None'):
          first_val = 1# Edit None Value here
        else:
          first_val = int(e_ele['value'][0])
      elif(e_ele['name'] == second_var):
        second_val = int(e_ele['value'][1])

    """ Grade by our rules """
    grade = first_val * second_val
    node[node_id]['grade'] += grade

  return node

def getWeightList(weight_file):
  """ Read Weight.json """
  src = open(weight_file)
  content = json.loads(src.read())
  src.close()

  """ Convert to int """
  for idx in content:
    content[idx] = int(content[idx])

  return content


