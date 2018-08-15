# Frequency Binning Schemes
There were 1024 frequency bins for every spectrogram. With a maximum frequency of 5000 Hz, each bin covered a range of about 4.88 Hz of frequency.
## Scheme 1
*First exploration of frequency binning. All following schemes are based on this.*

Bin 0 to 20: average by a factor of 10

Bin 20 to 123: do not average

Bin 123 to 533: average by a factor of 10

Bin 533 to 634: do not average

Bin 634 to 1024: average by a factor of 10

**This results in 286 bins, down from the original 1024. Reduction by a factor of about 4.**

## Scheme 2
*Everything is averaged by some factor here. Some regions see coarser averaging, while others are finer.*

Bin 0 to 20: average by a factor of 20

Bin 20 to 124: average by a factor of 2

Bin 124 to 524: average by a factor of 20

Bin 524 to 634: average by a factor of 2

Bin 634 to 774: average by a factor of 20

Bin 774 to 864: average by a factor of 10

Bin 864 to 1024: average by a factor of 20

**This results in 152 bins, a factor of 2 reduction from scheme1.**

## Scheme 3
*Further tweaking averaging factors. This was the final frequency binning scheme applied to the data before time binning was done.*

Bin 0 to 20: average by a factor of 20

Bin 20 to 124: average by a factor of 2

Bin 124 to 524: average by a factor of 20

Bin 524 to 632: average by a factor of 4

Bin 632 to 634: average by a factor of 2

Bin 634 to 774: average by a factor of 20

Bin 774 to 864: average by a factor of 10

Bin 864 to 1024: average by a factor of 20

**125 bins with this scheme.**
