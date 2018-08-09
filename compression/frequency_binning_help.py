def freq_range_from_bin(bin, cadence):
    end = bin * cadence
    start = end - cadence
    return start, end

def bin_from_freq_range(end_freq, cadence):
    bin = end_freq / cadence
    return bin

def value_range_from_bin(bin, rate):
    rate = rate - 1
    end = (bin * rate) + (bin - 1)
    start = end - rate
    return start, end
