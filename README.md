# labelle_to_dRF
Import LaBelle group RF binary data into MIT Haystack digital_rf container format.
Done for early stages of AERO satellite project.

##What does this do?
LaBelle group data consists of multiple-GB binary files, containing 2 or 4 channels of 2 byte integers. Data start and end time metadata is stored in the filename, and sample rate is stored in LaBelle notes.
These Python programs take the binary LaBelle data and write it in the digital_rf format, a MIT Haystack standard for data storage.
digital_rf is designed to be future-proof, so it has stringent standards for storing metadata. This program parses metadata (both from the filename and user) and stores it in the digital_rf standard.

###convert_ant_individually.py
This program allows the user to specify the channel (which corresponds to antenna) they want to extract from the LaBelle data and convert to digital_rf. It is useful when only a specific channel is desired in digital_rf format.

###convert_ant_to_channels.py
This program converts all channels in the LaBelle data to corresponding digital_rf channels. It is useful when all channels are of interest, or for a complete data conversion to digital_rf.
