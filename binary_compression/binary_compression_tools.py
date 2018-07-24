import numpy as np

def read_txt_into_array(path):
    """Return data as a numpy array."""
    f = open(path, 'r')
    temp1 = []
    temp2 = []
    for line in f:
        temp1.append(line)
    for b in temp1:
        b.replace('\n', '')
        temp2.append(float(b))
    temp = None
    data = np.float64(np.array(temp2))
    return data

#begin test program
path_to_psd_data = '/home/anoush/Desktop/working/psd.txt'
print(read_txt_into_array(path_to_psd_data))
