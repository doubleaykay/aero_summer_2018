import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("-r", "--reduce", nargs='?', const=True, type=bool, default=True, help="use this flag to suppress expanding the compressed data")
# parser.add_argument("-r", "--reduce", nargs='?', help="use this flag to suppress expanding the compressed data")
parser.add_argument('-r', '--reduce', action='store_false')
args = parser.parse_args()

# if ( args.reduce == None ):
#     expand = True
# else:
#     expand = False

print('This will always print')
if args.reduce:
    print('This will print if -r is true')
else:
    print('This will print if -r is false')
