import sys
import re
import json
import pprint

""" Load Setting.json, and then generate the GPU device list """
def genGPUList(setting_file):
  print 'Generate GPU device list'

  """ Read Setting.json """
  src = open(setting_file)
  content = json.loads(src.read())
  src.close()

""" Cut the meta file """
def analyzeMetaFile(meta_file):
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

  for str in lines:
    """ Find __node__ function """
    if(flag or re.match('__node__', str)):
      """ First access """
      if(not flag):
        flag = True
        meta['node'].append([])

      meta['node'][node_idx].append(str)

      """ Last access """
      if(re.match('}', str)):
        flag = False
        node_idx += 1

  """ Get execute part """
  """ Initialize variables for get execute part """
  flag = False
  execute_idx = 0

  for str in lines:
    """  """
    if(execute_idx == node_idx):
      meta['execute'].append(str)

    """ Find __node__ function """
    if(flag or re.match('__node__', str)):
      """ First access """
      if(not flag):
        flag = True

      """ Last access """
      if(re.match('}', str)):
        flag = False
        execute_idx += 1


  """ Debug """
  pprint.pprint(meta)

