import os
import argparse
import numpy as np

"""
List sizes in bytes of all 'psd.dat' files in a root directory.
"""

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', help='root directory')
args = parser.parse_args()

root_dir = args.dir
a = []
for root, dirs, files in os.walk(root_dir):
        for file in files:
            p=os.path.join(root,file)
            a.append(os.path.abspath(p))

# keep only paths for 'psd.dat' files
b = [s for s in a if 'psd.dat' in s]
b = np.sort(b)

sizes = []
for k in b: sizes.append(os.path.getsize(k))
print(sizes)
