import numpy as np
import sys
import argparse
import os
import datetime
import dateutil.parser


#print(dateutil.parser.parse('2018-06-23T00:00:00'))
filename = '20180506-0823-0840-TLK-INT'

UTstart = dateutil.parser.parse(filename.split("-")[0] + filename.split("-")[1])
epoch = dateutil.parser.parse('1970, 1, 1')
sec_since_epoch = int((UTstart - epoch).total_seconds())
samples_since_epoch = sec_since_epoch * 10000000
print(sec_since_epoch)
print(samples_since_epoch)

# UTdate = filename.split("-")[0]
# UTstart = filename.split("-")[1]
# UTend = filename.split("-")[2]
#
# print(UTdate)
# print(UTstart)
# print(UTend)
#
#
#
# start_date_and_time = UTdate + UTstart
# test = dateutil.parser.parse(start_date_and_time)
# print(test)
# #print(timegm(dateutil.parser.parse(UTdate)))
#
# epoch = dateutil.parser.parse('1970, 1, 1')
# sec = int((test - epoch).total_seconds())
# print(sec)
#
# y = int(datetime.datetime.strptime(str(UTdate), '%Y%m%d').strftime('%Y'))
# m = int(datetime.datetime.strptime(str(UTdate), '%Y%m%d').strftime('%m'))
# d = int(datetime.datetime.strptime(str(UTdate), '%Y%m%d').strftime('%d'))
# h = int(datetime.datetime.strptime(str(UTstart), '%H%M').strftime('%H'))
# M = int(datetime.datetime.strptime(str(UTstart), '%H%M').strftime('%M'))
#
# sec_since_epoch = int((datetime.datetime(y,m,d,h,M) - datetime.datetime(1970,1,1)).total_seconds())
# print(sec_since_epoch)
#
# if sec == sec_since_epoch:
#     print('They are equal')

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

# file = sys.argv[1]
# type = np.dtype('u2, u2, u2, u2')
#
# def read_in_chunks(file_object, chunk_size=1024):
#     while True:
#         data = file_object.read(chunk_size)
#         if not data:
#             break
#         yield data
#
# f = open(file, 'r')
# for piece in read_in_chunks(f):
#     data = np.frombuffer(piece, type, count=-1)
#     print(data)

# parser = argparse.ArgumentParser()
# parser.add_argument("-v", "--verbose", help="print everything")
# args = parser.parse_args()
#
# if args.verbose:
#     print('Verbose mode on')
# else:
#     print('Verbose mode off')
#
# start_time = datetime.datetime.now()
# print(str(start_time))
# try:
#     input("Press enter to continue")
# except SyntaxError:
#     pass
# end_time = datetime.datetime.now()
# print(str(end_time))
# print('Time elapsed:' + str(end_time - start_time))
