import numpy as np

def compression_diffs(reference, compressed):
    scale_factor = np.maximum(reference) / np.maximum(compressed)
    diffs = []
    for b in compressed:
        diffs.append(b * scale_factor)
    diffs = np.array(diffs)
    return diffs
