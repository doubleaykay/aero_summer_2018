import numpy as np

def read_txt_into_array(path):
    """Return data as a numpy array."""
    f = open(path, 'r')
    temp = []
    for line in f:
        temp.append(float(line.replace('\n', '')))
    data = np.float64(np.array(temp))
    temp = None
    return data

#begin test program
path_to_psd_data = '/home/anoush/Desktop/working/psd.txt'
print(read_txt_into_array(path_to_psd_data))
