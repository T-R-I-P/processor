import sys
import re
import json
import pprint

""" Load Setting.json, and then generate the GPU device list """
def getGPUList(setting_file):
  print 'Get GPU device list'

  """ Read Setting.json """
  src = open(setting_file)
  content = json.loads(src.read())
  src.close()

def getWeightList(weight_file):
  print 'Get weight list'

  """ Read Weight.json """
  src = open(weight_file)
  content = json.loads(src.read())
  src.close()

""" Cut the meta file """
def analyzeMetaFile(meta_file, weight_list):
  print 'Analyze the meta file'

  """ Initialize variables """
  meta = {}
  meta['header'] = []
  meta['node'] = []
  meta['execute'] = []

  """ Read meta file """
  src = open(meta_file)
  content = src.read()
  src.close()

  """ Cut file to line by line """
  lines = re.split('\n', content)

  """ Get header """
  for str in lines:
    if(re.match('import', str)):
      meta['header'].append(str)

  """ Get node """
  """ Initialize variables for get node """
  flag = False
  node_idx = 0
  count_paranthese = 0

  for str in lines:
    if(flag or re.match('__node__', str)):
      """ First access """
      if(not flag):
        flag = True
        count_paranthese = 1
        meta['node'].append([])

      meta['node'][node_idx].append(str)

      """ Count big parantheses to check whether end or not """
      if(re.match('{', str)):
        count_paranthese += 1
      if(re.match('}', str)):
        count_paranthese -= 1

      """ Last access """
      if((re.match('}', str)) and (count_paranthese == 0)):
        flag = False
        node_idx += 1

  """ Get execute part """
  """ Initialize variables for get execute part """
  flag = False
  execute_idx = 0

  for str in lines:
    if(execute_idx == node_idx):
      meta['execute'].append(str)

    """ Find __node__ function """
    if(flag or re.match('__node__', str)):
      """ First access """
      if(not flag):
        flag = True
        count_paranthese = 1

      """ Count big parantheses to check whether end or not """
      if(re.match('{', str)):
        count_paranthese += 1
      if(re.match('}', str)):
        count_paranthese -= 1

      """ Last access """
      if((re.match('}', str)) and (count_paranthese == 0)):
        flag = False
        execute_idx += 1


  """ Debug """
  pprint.pprint(meta)

