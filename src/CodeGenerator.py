# Our Library
import Utils

""" Generate the optimization code """
def genOptimization(raw, opt_setting, setting_file, benchmark_file, output_file):
  header = raw['header']
  node = raw['node']
  execute = raw['execute']

  setting = Utils.getSetting(setting_file, 'clusters')
  benchmark = Utils.getBenchmarkResult(setting_file, benchmark_file)
  content = ''

  content += '#!/usr/bin/env python\n\n'
  """ Concat header """
  content += header + '\n\n'

  """ Concat node """
  for idx, e in enumerate(opt_setting):
    node_id = e['node_id']
    host_id = e['host_id']
    benchmark_id = e['benchmark_id']

    """ example string: """
    """ with tf.device('/job:worker/task:1/gpu:0'):') """
    content += 'with tf.device(\'/job:worker/task:' + str(host_id)
    content += benchmark['all'][benchmark_id]['device-name']+ '\'):\n'
    content += node['node'][node_id]['content']
  content += '\n\n'


  """ Initialize Tensorflow """
  content += 'worker = ['
  for idx, e in enumerate(setting):
    if(idx != 0):
      content += ','
    content += '"' + e['host'] + ':' + str(e['port']) + '"'
  content += ']\n'

  content += 'cluster = tf.train.ClusterSpec({"worker":worker})\n\n'

  """ Concat execute """
  content += execute

  Utils.saveFile(output_file, content)

