#!/usr/bin/env python
#argv = Setting.json, Meta Language File

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

""" Parser """
print '====== Parser ======'
""" Generate a object from the meta file          """
""" meta (object)                                 """
""" |                                             """
""" |---- header (string)                         """
""" |                                             """
""" |---- node   (object)                         """
""" |     |                                       """
""" |     |--- device (object)                    """
""" |     |    |                                  """
""" |     |    |--- [device_id] (array)           """
""" |     |         {                             """
""" |     |           'node_id': [node_id]        """
""" |     |         }                             """
""" |     |                                       """
""" |     |--- ele (array)                        """
""" |     |    {                                  """
""" |     |      'content': [source string]       """
""" |     |      'lines': [source lines]          """
""" |     |      'device_id': [device_id]         """
""" |     |      'grade': [grade]                 """
""" |     |    }                                  """
""" |     |                                       """
""" |     |--- variable (object)                  """
""" |          |                                  """
""" |          |--- matmul (array)                """
""" |          |    {                             """
""" |          |      'type':                     """
""" |          |      'value': [X, Y1]            """
""" |          |    }                             """
""" |          |                                  """
""" |          |--- ele (array)                   """
""" |          |    {                             """
""" |          |      'type':                     """
""" |          |      'value': [None, 100]        """
""" |          |    }                             """
""" |                                             """
""" |---- execute (string)                        """
meta = Parser.analyzeMetaFile(meta_file)


""" Evaluator """
print '====== Evaluator ======'
""" Find the optimization setting """
optimization_setting = Evaluator.getOptimization(setting_file, weight_file, benchmark_file, meta)


""" Code Generator """
print '====== Code Generator ======'
""" Generate the optimization code """
CodeGenerator.genOptimization(optimization_setting)

