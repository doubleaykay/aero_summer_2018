import numpy as np

def as_numpy(filename):
    if '.txt' in filename:
        out = filename[:-4]
    else:
        raise ValueError('Based on provided filename, input is not a text file.')

    f = open(out, 'wb+')
    np.loadtxt(filename).tofile(f)
    f.close()

    print('Success.')

def as_py(filename):
    if '.txt' in filename:
        out = filename[:-4]
    else:
        raise ValueError('Based on provided filename, input is not a text file.')

    with open(filename) as f:
        raw = f.readlines()

    raw2 = []
    for a in raw:
        raw2.append(int(a.translate(None, '\n')))

    # print(raw2)

    g = open(out, 'wb+')
    g.write(bytearray(raw2))
    g.close()

    print('Success.')
