import os

"""Python module for working with LaBelle group data files"""

def get_filename(n):
    """Parse provided path to get filename. Provide path as string argument."""
    file = n
    path =  os.path.splitext(file)[0]
    filename = path.split("/")[path.count('/')]
    return filename
