#!/usr/bin/env python
#argv = Setting.json, Meta Language File, Weight, Benchmark Result, Output

# System Imports
import sys

# Our Library
import Parser
import Evaluator
import CodeGenerator
import Utils

# TensorFlow Inports
import tensorflow as tf

# For Debug
import pprint

""" Parameter Initialization """
setting_file = sys.argv[1] if len(sys.argv)>1 else '../data/Setting.json'
meta_file = sys.argv[2] if len(sys.argv)>2 else '../data/File.meta'
weight_file = sys.argv[3] if len(sys.argv)>3 else '../data/Weight.json'
benchmark_file = sys.argv[4] if len(sys.argv)>4 else '../data/benchmark_result.json'
output_file = sys.argv[5] if len(sys.argv)>5 else 'output.py'

""" Parser """
print '====== Parser ======'
""" Generate a object from the meta file          """
""" raw (object)                                  """
""" |                                             """
""" |---- header (string)                         """
""" |                                             """
""" |---- execute (string)                        """
""" |                                             """
""" |---- node   (object)                         """
""" |     |                                       """
""" |     |--- node (array)                       """
""" |     |                                       """
""" |     |    index is node_id                   """
""" |     |    Each Element                       """
""" |     |    {                                  """
""" |     |      'content': [source string]       """
""" |     |      'lines': [source lines]          """
""" |     |      'device_id': [device_id]         """
""" |     |      'grade': [grade]                 """
""" |     |    }                                  """
""" |     |                                       """
""" |     |--- variable (array)                   """
""" |     |                                       """
""" |     |    Each Element                       """
""" |     |    {                                  """
""" |     |      'name': [name]                   """
""" |     |      'type': matmul, placeholder ...  """
""" |     |      'value': [None, 100], or [x, y_] """
""" |     |    }                                  """

(raw, data) = Parser.analyzeMetaFile(meta_file)

""" Evaluator """
print '====== Evaluator ======'
""" Find the optimization setting """
opt_setting = Evaluator.getOptimization(weight_file, setting_file, benchmark_file, data)


""" Code Generator """
print '====== Code Generator ======'
""" Generate the optimization code """
CodeGenerator.genOptimization(raw, opt_setting, setting_file, benchmark_file, output_file)

