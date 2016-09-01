#!/usr/bin/env python

import os

"""
Functions for extracting data from file paths produced by
the ImageXpress.

NOTE:
     These functions will not work if the plate name contains an underscore
     Also, assumes the well was imaged with multiple sites
"""


def only_tifs(x):
    """Returns a list of filenames that are .tifs"""
    images = []
    with open(x) as f:
        for line in f:
            if ".tif" in line:
                images.append(str(line))
    return images


def get_filename(x):
    """ Get the final image URL"""
    files = []
    with open(x) as f:
        for line in f:
            filename = str(line.split(os.sep)[-1])
            files.append(filename.strip())
    return files


def check_filename(x, char="_"):
    """
    Sanity check for list of filenames
    - check it's not an empty line
    - see if length when split == 4
    """
    for f in x:
        # if length of file less than 20 characters
        if len(f) < 20:
            raise ValueError("Filename {} too short".format(f))
        # if not split into 4 by underscores, then missing a metadata
        # category, i.e no site information is present
        if len(f.split(char)) < 4:
            raise ValueError("Filename {} contains too few metadata values".format(f))


def get_path(x):
    """Get the path up until the image URL"""
    paths = []
    with open(x) as f:
        for line in f:
            p, f = os.path.split(line)
            paths.append(p.strip())
    return paths


def get_platenum(x):
    """ Get the platenumber"""
    plates = []
    with open(x) as f:
        for line in f:
            plates.append(int(line.split(os.sep)[-2]))
    return plates


def get_platename(x):
    """Get the user-defined plate name"""
    plates = []
    with open(x) as f:
        for line in f:
            plates.append(line.split(os.sep)[-4])
    return plates


def get_date(x):
    """Get the date of imaging for a plate"""
    dates = []
    with open(x) as f:
        for line in f:
            dates.append(line.split(os.sep)[-3])
    return dates


def split_filename(x, char ="_"):
    """Split filename by character"""
    url = get_filename(x)
    filename = []
    for line in url:
        filename.append(line.split(char))
    return filename


def get_metadata_well(x, char="_"):
    """Return well labels from filepaths"""
    url = get_filename(x)
    wells = []
    for line in url:
        x = str(line.split(char)[1])
        wells.append(x)
    return wells


def get_metadata_site(x, char="_"):
    """Return imaging sites from filepaths"""
    url = get_filename(x)
    sites = []
    for line in url:
        site_str = line.split(char)[2]
        site_num = int("".join(x for x in site_str if x.isdigit()))
        sites.append(site_num)
    return sites


def get_metadata_channel(x, char="_"):
    """Return channel numbers from file paths
       note: assumes channel numbers never exceed 9"""
    url = get_filename(x)
    channels = []
    for line in url:
        ch = int(line.split(char)[3][1])
        channels.append(ch)
    return channels
