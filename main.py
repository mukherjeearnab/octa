import sys

import strings
import auxiliary

import init
import add
import commit

if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        init.run()
    elif sys.argv[1] == 'add':
        add.run()
    elif sys.argv[1] == 'commit':
        commit.run()
    else:
        print("Invalid arguments:", sys.argv[1])
        auxiliary.showHelp()
else:
    auxiliary.showHelp()
