import os
import argparse

# #make directories to match number of antennas
# #number_of_antennas = int(args.antenna)
# number_of_antennas = 4
# i = 0
# while i <= (number_of_antennas - 1):
#     dir = ("/home/anoush/Desktop/working" + "/ant" + str(i))
#     os.makedirs(dir)
#     i += 1

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of file to read from")
args = parser.parse_args()

if args.input == "hello":
    print("Hi Anoush!")
if args.input == "test":
    print("Testing.")
