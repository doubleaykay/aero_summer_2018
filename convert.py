import digital_rf as drf
import sys
import os

path =  os.path.splitext(sys.argv[1])[0] #path with no extension from command line argument
filename = path.split("/")[4]
#print(filename) #debug if filename is correct

date = filename.split("-")[0]
UTstart = filename.split("-")[1]
UTend = filename.split("-")[2]
