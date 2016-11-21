#!/usr/bin/env python
#argv = Setting.json

import sys
import json

setting_file = sys.argv[1]

src = open(setting_file)
content = json.loads(src.read())
src.close()

print '====== Benchmark ======'

