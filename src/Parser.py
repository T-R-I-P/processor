import sys
import re
import json
import pprint

def getWeightList(weight_file):
  print 'Get weight list'

  """ Read Weight.json """
  src = open(weight_file)
  content = json.loads(src.read())
  src.close()

  """ Convert to int """
  for idx in content:
    content[idx] = int(content[idx])

  return content

""" Cut the meta file """
def analyzeMetaFile(meta_file, weight_list):
  print 'Analyze the meta file'

  """ Initialize variables """
  meta = {}

  """ Read meta file """
  src = open(meta_file)
  content = src.read()
  src.close()

  """ Cut file to line by line """
  lines = re.split('\n', content)

  """ Get part of header """
  meta['header'] = getHeader(lines)

  """ Get part of node function """
  (node_content, count_node) = getNodeFunction(lines)
  meta['node'] = analyzeNodeFunction(node_content, weight_list)

  """ Get part of execute """
  meta['execute'] = getExecute(lines, count_node)

  #Debug
  pprint.pprint(meta)

  return meta

def getHeader(lines):
  result = ''

  """ Get header """
  for str in lines:
    if(re.match('import', str)):
      result += str + '\n'

  return result

def getNodeFunction(lines):
  """ Initialize variables for get node """
  flag = False
  node_idx = ''
  count_node = 0
  count_paranthese = 0
  node_content = {}

  for str in lines:
    if(flag or re.match('__node__', str)):
      """ First access """
      if(not flag):
        flag = True
        count_paranthese = 1
        node_idx = re.search(r'\((.*?)\)', str).group(1)
        node_content[node_idx] = []
        continue

      """ Last access """
      if((re.match('}', str)) and (count_paranthese == 1)):
        flag = False
        count_node += 1
        continue

      """ Count big parantheses to check whether end or not """
      if(re.match('{', str)):
        count_paranthese += 1
      if(re.match('}', str)):
        count_paranthese -= 1

      """ Append new line """
      node_content[node_idx].append(str)

  return (node_content, count_node)

def getExecute(lines, count_node):
  """ Initialize variables for get execute part """
  flag = False
  execute_idx = 0
  result = ''

  for str in lines:
    if(execute_idx == count_node):
      result += str + '\n'
      continue

    """ Find __node__ function """
    if(flag or re.match('__node__', str)):
      """ First access """
      if(not flag):
        flag = True
        count_paranthese = 1
        continue

      """ Last access """
      if((re.match('}', str)) and (count_paranthese == 1)):
        flag = False
        execute_idx += 1
        continue

      """ Count big parantheses to check whether end or not """
      if(re.match('{', str)):
        count_paranthese += 1
      if(re.match('}', str)):
        count_paranthese -= 1

  return result

def analyzeNodeFunction(node_content, weight_list):
  result = {}

  """ Get variables """
  for idx in node_content:
    result[idx] = {}
    result[idx]['weight_grade'] = 0

    for str in node_content[idx]:
      """ Count grade """
      for weight_element in weight_list:
        if(re.search(weight_element, str)):
          print str
          result[idx]['weight_grade'] += weight_list[weight_element]

  return result

