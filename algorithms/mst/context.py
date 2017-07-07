import os
import sys

parentFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, parentFolder)

import structures

if __name__ == '__main__':
    print("Used for importing the structures package")