import numpy as np

def as_numpy(filename):
    if '.txt' in filename:
        out = filename[:-4]
    else:
        raise ValueError('Based on provided filename, input is not a text file.')

    a = np.loadtxt(filename, 'i1')
    b = a.reshape((-1,2))

    b[:,1] = b[:,1] << 4

    c = np.bitwise_or(b[:,0], b[:,1]).astype('i1')

    f = open(out, 'wb+')
    c.tofile(f)
    f.close()

    print('Success.')
