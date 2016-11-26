# Our Library
import Utils

""" Generate the optimization  """
def genOptimization(raw, opt_setting, benchmark_file, output_file):
  print 'Generate the optimization'
  header = raw['header']
  node = raw['node']
  execute = raw['execute']

  benchmark = Utils.getBenchmarkResult(benchmark_file)
  content = ''

  """ Concat header """
  content += header + '\n'

  """ Concat node """
  for idx, e in enumerate(opt_setting):
    node_id = e['node_id']
    benchmark_id = e['benchmark_id']

    content += node['node'][node_id]['content']

  """ Concat execute """
  content += execute

  Utils.saveFile(output_file, content)

