import numpy as np
import sys


# test = [1, 2, 3]
# print(np.array(test))
#
# test.append(4)
# print(np.array(test))

# hello = []
#
# def function(i):
#     if(i<10):
#         hello.append(i)
#         print(np.array(hello))
#         function(i+1)
#     else:
#         list = [0]
#         print(np.array(hello))
#
# function(1)

# antenna = (input("What antenna do you want to read from? ") - 1)
# if(antenna >= 5):
#     print("There are only 4 antennas. Please enter a number from 1 to 4.")
#     antenna = (input("What antenna do you want to read from? ") - 1)
#     print(antenna)
# else:
#     print(antenna)

file = sys.argv[1]
type = np.dtype('u2, u2, u2, u2')

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

f = open(file, 'r')
for piece in read_in_chunks(f):
    data = np.frombuffer(piece, type, count=-1)
    print(data)
