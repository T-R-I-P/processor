#!/usr/bin/env python
#argv = Setting.json, Meta Language File

import sys

import Parser
import Evaluator
import CodeGenerator
import Utils

""" Parameter Initialization """
setting_file = sys.argv[1]
meta_file = sys.argv[2]
weight_file = sys.argv[3]

""" Load Setting.json """
worker_hosts = Utils.getSetting(setting_file, "clusters")

""" Parser """
print '====== Parser ======'

""" Load Weight.json """
weight_list = Parser.getWeightList(weight_file)

""" Generate a object from the meta file """
meta = Parser.analyzeMetaFile(meta_file, weight_list)

""" Evaluator """
print '====== Evaluator ======'
""" Find the optimization setting """
optimization_setting = Evaluator.getOptimization(worker_hosts, meta)

""" Code Generator """
print '====== Code Generator ======'
""" Generate the optimization code """
CodeGenerator.genOptimization(optimization_setting)

