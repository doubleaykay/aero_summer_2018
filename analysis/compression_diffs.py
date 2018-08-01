import numpy as np

def compression_diffs(reference, compressed):
    scale_factor = np.amax(reference) / np.amax(compressed)
    scaled = []
    for b in compressed:
        scaled.append(b * scale_factor)

    diffs = []
    if len(reference) == len(scaled):
        i = 0
        while i <= (len(reference) -1):
            value = abs(reference[i] - scaled[i])
            diffs.append(value)
            i += 1
    else:
        print('Arrays are not equal in length.')

    diffs = np.array(diffs)
    return diffs
