# System Imports
import sys
import re
import json

# Our Library
import Structure

# For Debug
import pprint

""" Cut the meta file """
def analyzeMetaFile(meta_file):
  print 'Analyze the meta file'

  """ Initialize variables """
  raw = {}

  """ Read meta file """
  src = open(meta_file)
  content = src.read()
  src.close()

  """ Cut file to line by line """
  lines = re.split('\n', content)

  """ Get part of header """
  raw['header'] = getHeader(lines)

  """ Get part of execute """
  raw['execute'] = getExecute(lines)

  """ Get part of node function """
  node = getNode(lines)

  """ Restructure node """
  raw['node'] = analyzeNode(node)

  """ Wrapper to a class FOR GOOD API """
  node = wrapClass(raw['node']['node'], raw['node']['variable'])

  return (raw, node)

def getHeader(lines):
  result = ''

  """ Get header """
  for str in lines:
    if(re.match('import', str)):
      result += str + '\n'

  return result

def getNode(lines):
  """ Initialize variables for get node """
  flag = False
  device_id = ''
  count_paranthese = 0
  node = []
  content = {}

  for str in lines:
    if(flag or re.match('__node__', str)):
      """ First access """
      if(not flag):
        flag = True
        count_paranthese = 1
        device_id = re.search(r'\((.*?)\)', str).group(1)

        content = {}
        content['content'] = ''
        content['lines'] = []
        content['device_id'] = device_id
        continue

      """ Last access """
      if((re.match('}', str)) and (count_paranthese == 1)):
        flag = False
        node.append(content)
        continue

      """ Count big parantheses to check whether end or not """
      if(re.match('{', str)):
        count_paranthese += 1
      if(re.match('}', str)):
        count_paranthese -= 1

      """ Append new line """
      content['content'] += str + '\n'
      content['lines'].append(str)

  return node

def getExecute(lines):
  """ Initialize variables for get execute part """
  flag = False
  count_paranthese = 0
  result = ''

  for str in lines:
    """ Find __execute__ function """
    if(flag or re.match('__execute__', str)):
      """ First access """
      if(not flag):
        flag = True
        count_paranthese = 1
        continue

      """ Last access """
      if((re.match('}', str)) and (count_paranthese == 1)):
        flag = False
        continue

      """ Count big parantheses to check whether end or not """
      if(re.match('{', str)):
        count_paranthese += 1
      if(re.match('}', str)):
        count_paranthese -= 1

      result += str + '\n'

  return result

def analyzeNode(node):
  r_node = {}
  variable = []
  new_variable = {}
  first_equal_op = 0
  left_value = ''
  right_value = ''
  tmp = ''
  src = ''

  for idx, content in enumerate(node):
    content['grade'] = 0

    for str in content['lines']:
      """ Get variable """
      """ Find first equal operator """
      first_equal_op = str.find('=')
      left_value = str[0:(first_equal_op-1)]
      right_value = str[(first_equal_op+1):len(str)]

      """ Remove all spaces and tabs """
      left_value = re.sub('[\s+]', '', left_value)
      right_value = re.sub('[\s+]', '', right_value)

      new_variable = {}
      new_variable['node_id'] = idx
      new_variable['device_id'] = content['device_id']
      new_variable['name'] = left_value

      if(re.search('matmul', str)):
        new_variable['type'] = 'matmul'
        tmp = re.search(r'matmul\((.*?)\)', right_value).group(1)
        new_variable['value'] = tmp.split(',')
      elif(re.search('random_uniform', str)):
        new_variable['type'] = 'random_uniform'
        tmp = re.search(r'random_uniform\(\[(.*?)\]\)', right_value).group(1)
        new_variable['value'] = tmp.split(',')
      elif(re.search('placeholder', str)):
        new_variable['type'] = 'placeholder'
        tmp = re.search(r'placeholder\(.*?\[(.*?)\]\)', right_value).group(1)
        new_variable['value'] = tmp.split(',')
      else:
        continue

      variable.append(new_variable)

    node[idx] = content

  r_node['node'] = node
  r_node['variable'] = variable

  return r_node

def wrapClass(raw_node, raw_var):
  node = Structure.Node()

  for node_id, e in enumerate(raw_node):
    node.addNode(node_id, e['device_id'], e['content'], e['lines'])

  for idx, e in enumerate(raw_var):
    node.addVariable(e['node_id'], e['name'], e['type'], e['value'])

  return node

