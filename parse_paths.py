import os


def get_filename(file_list):
    """return the final image URLS from a file path"""
    files = []
    for line in file_list:
        filename = str(line.split(os.sep)[-1])
        files.append(filename.strip())
    return files


def check_filename(file_list, char="_"):
    """sanity check list of filenames"""
    for f in file_list:
        if len(f) < 20:
            raise ValueError("Filename {} too short".format(f))
        # get just the filename and check for metadata values
        filename = str(f.split(os.sep)[-1])
        if len(filename.split(char)) < 4:
            raise ValueError("Filename {} contains too few metadata values".format(f))


def get_path(file_list):
    """return the path up until the image URL"""
    paths = []
    for line in file_list:
        p, f = os.path.split(line)
        paths.append(p.strip())
    return paths


def get_platename(file_list):
    """return platename from file path"""
    plates = []
    for line in file_list:
        plates.append(line.split(os.sep)[-4])
    return plates


def get_platenum(file_list):
    """return plate number"""
    plates = []
    for line in file_list:
        plates.append(line.split(os.sep)[-2])
    return plates


def get_date(file_list):
    """return date of imaging for a plate"""
    dates = []
    for line in file_list:
        dates.append(line.split(os.sep)[-3])
    return dates


def split_filename(file_list, char="_"):
    """split filename by characher"""
    url = get_filename(file_list)
    filename = []
    for line in url:
        filename.append(line.split(char))
    return filename


def get_metadata_well(file_list, char="_"):
    """return well labels from file paths"""
    url = get_filename(file_list)
    wells = []
    for line in url:
        wells.append(str(line.split(char)[1]))
    return wells


def get_metadata_site(file_list, char="_"):
    """return imaging sites/field-of-view from filepaths"""
    url = get_filename(file_list)
    sites = []
    for line in url:
        site_str = line.split(char)[2]
        site_num = int("".join(x for x in site_str if x.isdigit()))
        sites.append(site_num)
    return sites


def get_metadata_channel(file_list, char="_"):
    """return channel numbers from file paths"""
    url = get_filename(file_list)
    channels = []
    for line in url:
        ch = int(line.split(char)[3][1])
        channels.append(ch)
    return channels

