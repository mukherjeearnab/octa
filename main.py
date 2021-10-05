import sys

import strings
import auxiliary

if len(sys.argv) > 1:
    print("OK")
else:
    auxiliary.logMessage("Usage:", strings.STRS['HELP'])
