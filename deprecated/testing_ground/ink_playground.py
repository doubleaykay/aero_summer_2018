def opposite_number(num, center):
    diff = num - center
    if (diff) < 0:
        # center is bigger
        opposite = center + abs(diff)
    if (diff) > 0:
        # center is smaller
        opposite = center - abs(diff)
    if num == center:
        opposite = num
    return opposite
