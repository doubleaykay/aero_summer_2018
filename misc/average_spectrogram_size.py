import os

def list_files_in_dir(root_dir):
    """Return a list of all file paths within a directory, including files in subdirectories. Pass in directory path as string."""

def average_file_size(file_list):
    """Return average file size in bytes of numerous files. Pass in file paths as a list."""
    file_size_list = []
    i = 0
    while i <= len(file_list) - 1:
        file_size_list.append(os.getsize(file_list[i]))
        i += 1
    average = (sun(file_size_list) / len(file_size_list))
    return average
