#!/usr/bin/env python

"""
Functions for extracting data from file paths produced by
the ImagXpress.

NOTE:
     These functions will not work if the plate name contains an underscore
"""


def only_tifs(x):
    """Returns a list of filenames that are .tifs"""
    images = []
    for line in open(x, "r").readlines():
        if ".tif" in line:
            images.append(str(line))
    return images

def get_filename(x):
    """ Get the final image URL"""
    files = []
    for line in open(x, "r").readlines():
        filename = str(line.split("/")[-1])
        files.append(filename)
    return files


def get_platenum(x):
    """ Get the platenumber"""
    plates = []
    for line in open(x).readlines():
        num = int(line.split("/")[-2])
        plates.append(num)
    return plates


def get_platename(x):
    """Get the user-defined plate name"""
    plates = []
    for line in open(x).readlines():
        plates.append(line.split("/")[-4])
    return plates


def get_date(x):
    """Get the date of imaging for a plate"""
    dates = []
    for line in open(x).readlines():
        dates.append(line.split("/")[-3])
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
    """Return channel numbers from file paths"""
    url = get_filename(x)
    channels = []
    for line in url:
        ch = int(line.split(char)[3][1])
        channels.append(ch)
    return channels


if __name__ == "__main__":
    [print(i) for i in get_filename("out_test.txt")]