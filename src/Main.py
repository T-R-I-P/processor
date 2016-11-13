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
""" Load Setting.json, and then generate the GPU device list """
gpu_list = Parser.genGPUList(setting_file)

""" Generate a file to execute """
Parser.genExecuteFile(meta_file)

""" Execute evaluator """

""" Execute code generator """

