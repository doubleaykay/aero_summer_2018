import os
import datetime
import dateutil.parser

"""Python module for working with LaBelle group data files."""

def get_filename(path):
    """Parse provided path to get filename. Provide path as string argument."""
    file = path
    path =  os.path.splitext(file)[0]
    filename = path.split("/")[path.count('/')]
    return filename

def get_epoch(filename):
    """Get seconds since epoch from provided filename, assuming standard LaBelle file naming scheme. Provide filename (not path) as string."""
    UTstart = dateutil.parser.parse(filename.split("-")[0] + filename.split("-")[1])
    epoch = dateutil.parser.parse('1970, 1, 1')
    sec_since_epoch = int((UTstart - epoch).total_seconds())
    return sec_since_epoch

def construct_dtype(antennas):
    """Construct numpy data type based on number of antennas in file. LaBelle data files are 16bit unsigned integers, which are represented by 'u2' in numpy. Provide number of antennas as an int argument."""
    type = ('u2,' * int(antennas))[:-1]
    return type
