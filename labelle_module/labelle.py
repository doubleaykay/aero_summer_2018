import os
import datetime
import dateutil.parser
import glob

"""Python module for working with LaBelle group data files."""

def get_filename(file):
    """Parse provided path to get filename. Provide path as string argument."""
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

def make_dirs(out_path, antennas):
    """Make appropriate antenna directories. Specify output dir as string, and number of antennas as int."""
    #check if output directory exists
    if not os.path.exists(out_path):
        print('Output directory does not exist, making it now...')
        os.makedirs(out_path)

    #make directories to match number of antennas
    number_of_antennas = int(antennas)
    i = 0
    while i <= (number_of_antennas - 1):
        dir = (out_path + "/ant" + str(i))
        if not os.path.exists(dir):
            os.makedirs(dir)
        i += 1
    print('Output directories created.')

def get_dat(dir):
    """Return list of all .dat LaBelle data files in given directory. Provide directory as string."""
    os.chdir(dir)
    all_dat = []
    for file in glob.glob("*.dat"):
        all_dat.append(file)
    return all_dat
