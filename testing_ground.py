import numpy as np

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

antenna = (input("What antenna do you want to read from? ") - 1)
if(antenna >= 5):
    print("There are only 4 antennas. Please enter a number from 1 to 4.")
    antenna = (input("What antenna do you want to read from? ") - 1)
    print(antenna)
else:
    print(antenna)
