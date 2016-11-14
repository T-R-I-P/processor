#!/usr/bin/env python
#argv = Setting.json, Meta Language File

import sys

import Parser
import Evaluator
import CodeGenerator

""" Parameter Initialization """
setting_file = sys.argv[1]
meta_file = sys.argv[2]

""" Parser """
print '====== Parser ======'
""" Load Setting.json, and then generate the GPU device list """
gpu_list = Parser.genGPUList(setting_file)

""" Generate a object from the meta file """
meta = Parser.analyzeMetaFile(meta_file)

""" Evaluator """
print '====== Evaluator ======'
""" Find the optimization setting """
optimization_setting = Evaluator.getOptimization(gpu_list, meta)

""" Code Generator """
print '====== Code Generator ======'
""" Generate the optimization code """
CodeGenerator.genOptimization(optimization_setting)

