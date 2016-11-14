import sys
import json

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

  """ Read meta file """
  src = open(meta_file)
  content = src.read()
  src.close()

  """ Get header """

  """ Get node """

  """ Get execute part """
