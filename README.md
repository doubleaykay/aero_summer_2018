[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# labelle_to_dRF
Import LaBelle group RF binary data into MIT Haystack digital_rf container format.
Done for early stages of AERO satellite project.

## What does this do?
LaBelle group data consists of multiple-GB binary files, containing 2 or 4 channels of 2 byte integers. Data start and end time metadata is stored in the filename, and sample rate is stored in LaBelle notes.
These Python programs take the binary LaBelle data and write it in the digital_rf format, a MIT Haystack standard for data storage.
digital_rf is designed to be future-proof, so it has stringent standards for storing metadata. This program parses metadata (both from the filename and user) and stores it in the digital_rf standard.

### convert_ant_individually.py
This program allows the user to specify the channel (which corresponds to antenna) they want to extract from the LaBelle data and convert to digital_rf. It is useful when only a specific channel is desired in digital_rf format.

### convert_ant_to_channels.py
This program converts all channels in the LaBelle data to corresponding digital_rf channels. It is useful when all channels are of interest, or for a complete data conversion to digital_rf.

## Usage
Options are specified via command-line arguments; see below for the command line options available for each program.

### Notes on Usage
* Input file must be a ".dat" file.
* If the output directory does not already exist, the program will create it for you.
* For the user, antenna numbers are indexed from 1 (i.e. antenna 1, antenna 2, etc). In the code, they are indexed from 0 (i.e. antenna 0, antenna 1, etc). So, "antenna 1" for the user corresponds to "antenna 0" in code.
* Because the LaBelle group data files are multiple-GB sized files, they can not be read into memory at once. So, the program reads the data in chunks, looping over the chunk size until the end of the file has been reached. The chunk size can be custom set; I find that a value of "40000000" bytes works well on a machine with 8GB of RAM.
* The binary data is read as a numpy array, so the data type must be specified. For 2 channel data, use "u2,u2". For 4 channel data, use "u2,u2,u2,u2". This may be auto-determined based on the number of antennas in the future.
* The sample rate is not specified in the filename, so it must be specified manually. Check against LaBelle group notes for sample rate.

### convert_ant_individually.py
Command Line Arguments:

```
-h, --help            show this help message and exit
-i INPUT, --input INPUT
                      location of file to read from
-o OUTPUT, --output OUTPUT
                      location of directory to output to
-a ANTENNA, --antenna ANTENNA
                      antenna number to read
-c CHUNK, --chunk CHUNK
                      chunk size to read in bytes
-d DTYPE, --dtype DTYPE
                      numpy data type
-r RATE, --rate RATE  sample rate in Hz
-v, --verbose         Print status messages to stdout.
```

* Output directory here be in the format "./{data_name}/ant#" where # is the user-facing antenna number (1-2 or 1-4)
* The specific user-facing antenna number to read from must be specified, not the total number of antennas.

### convert_ant_to_channels.py
Command Line Arguments:

```
-h, --help            show this help message and exit
-i INPUT, --input INPUT
                      location of file to read from
-o OUTPUT, --output OUTPUT
                      location of directory to output to
-a ANTENNAS, --antennas ANTENNAS
                      number of antennas in data
-c CHUNK, --chunk CHUNK
                      chunk size to read in bytes
-d DTYPE, --dtype DTYPE
                      numpy data type
-r RATE, --rate RATE  sample rate in Hz
-v, --verbose         Print status messages to stdout.
```

* Output directory must be in the format ```./{data_name}``` as channel names (ant#) as automatically determind from the number of antennas specified.
* The total user-facing number of antennas must be specified.
