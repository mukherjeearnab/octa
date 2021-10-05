import sys

import strings
import auxiliary

import init

if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        init.run()
    else:
        print("Invalid arguments:", sys.argv[1])
        auxiliary.showHelp()
else:
    auxiliary.showHelp()
