#!/usr/bin/env python

import sys
import subprocess

retcode = subprocess.call(['phpunit', '--process-isolation','.'])

sys.exit(retcode)
