import sys

import strings
import auxiliary

import init
import add

if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        init.run()
    elif sys.argv[1] == 'add':
        add.run()
    else:
        print("Invalid arguments:", sys.argv[1])
        auxiliary.showHelp()
else:
    auxiliary.showHelp()
