"""
Tests for path parsing functions
"""

# set up

from nose.tools import raises
import os
import sys
import glob
import shutil

CURRENT_PATH = os.path.dirname(__file__)
TEST_PATH = os.path.join(CURRENT_PATH, "example_dir")

def create_module_path():
    """need to import ImageList class from ../create_image_list.py"""
    module_path = os.path.realpath(os.path.join(CURRENT_PATH, ".."))
    sys.path.append(module_path)

create_module_path()

import parse_paths


# get file_paths from test directory
test_files = []
for name in glob.glob("example_dir/*/*/*/*tif"):
    test_files.append(name)

###############################################################################
#                             begin tests                                     #
###############################################################################

def test_get_filename():
    """parse_paths.get_filename returns only final file name"""
    output = parse_paths.get_filename(test_files)
    for i in output:
        assert i.startswith("val screen_")
        assert i.endswith(".tif")
    assert len(output) == len(test_files)


@raises(ValueError)
def test_check_filename():
    """parse_paths.check_filename returns error on too short filename"""
    # add in some dodgy file paths
    dodgy =  ["/too/short/path.jpg"]
    test_dodgy_file_paths = test_files + dodgy
    parse_paths.check_filename(test_dodgy_file_paths)


@raises(ValueError)
def test_check_filename2():
    """parse_paths.check_filename returns error on missing metadata"""
    # add in some dodgy file paths
    dodgy =  ["example_dir/test-plate-4/2015-08-01/4019/val screen_s4_w1324FDGDF435.tif"]
    test_dodgy_file_paths = test_files + dodgy
    parse_paths.check_filename(test_dodgy_file_paths)


def test_get_path():
    """parse_paths.get_path return path"""
    output = parse_paths.get_path(test_files)
    for i in output:
        assert not i.endswith(".tif")
    assert len(output) == len(test_files)


def test_get_platename():
    """parse_paths.get_platename returns correct platename"""
    names = parse_paths.get_platename(test_files)
    plate_names = ["test-plate-" + i for i in "1234"]
    for name in names:
        assert name in plate_names
    assert len(names) == len(test_files)
    assert len(set(names)) == 4


def test_get_platenum():
    """parse_paths.get_platenum returns correct platenum"""
    nums = parse_paths.get_platenum(test_files)
    plate_nums = ["4016", "4017", "4018", "4019"]
    for num in nums:
        assert num in plate_nums
    assert len(nums) == len(test_files)
    assert len(set(nums)) == 4


def test_get_date():
    """parse_paths.get_date returns correct date"""
    dates = parse_paths.get_date(test_files)
    plate_dates = ["2015-07-31", "2015-08-01"]
    print(dates)
    for date in dates:
        assert date in plate_dates
    assert len(dates) == len(test_files)
    assert len(set(dates)) == 2


def test_split_filename():
    """parse_paths.split_filename splits by character"""
    parse_paths.split_filename(test_files)


def test_get_metadata_well():
    """parse_paths.get_metadata_well returns correct wells"""
    wells = parse_paths.get_metadata_well(test_files)
    assert len(set(wells)) == 60
    assert len(wells) == len(test_files)


def test_get_metadata_site():
    """parse_paths.get_metadata_site returns correct sites"""
    sites = parse_paths.get_metadata_site(test_files)
    plate_sites = [int(i) for i in "123456"]
    assert len(sites) == len(test_files)
    assert len(set(sites)) == 6
    for site in sites:
        assert site in plate_sites


def test_get_metadata_channel():
    """parse_paths.get_metadata_channel returns correct channel"""
    channels = parse_paths.get_metadata_channel(test_files)
    plate_channels = [int(i) for i in "12345"]
    assert len(channels) == len(test_files)
    assert len(set(channels)) == 5
    for channel in channels:
        assert channel in plate_channels
