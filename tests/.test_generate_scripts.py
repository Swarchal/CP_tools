"""
Tests for generate_scripts
"""

import os
import sys

CURRENT_PATH = os.path.dirname(__file__)
def create_module_path():
    """need to import ImageList class from ../create_image_list.py"""
    module_path = os.path.realpath(os.path.join(CURRENT_PATH, ".."))
    sys.path.append(module_path)

create_module_path()

import shutil
import pandas
import subprocess

# set up
TEST_PATH = os.path.join(CURRENT_PATH, "example_dir")
RUNNING_LOCATION = os.path.realpath(os.path.join(CURRENT_PATH, ".."))
EXPERIMENT = TEST_PATH
LOADDATA_LOCATION = os.path.join(CURRENT_PATH, ".test_generate_scripts_loaddata")
PIPELINE = "/path/to/example/pipeline.cppipe"
PATH_PREFIX = "/exports/eddie/user"
SCRIPT_LOCATION = os.path.join(CURRENT_PATH, ".test_generate_scripts_scripts")

# run script from the command line with args
command = "python {}/generate_scripts.py \
--experiment {} \
--loaddata-location {} \
--pipeline {} \
--path-prefix {} \
--script-location {}".format(RUNNING_LOCATION,
                             EXPERIMENT,
                             LOADDATA_LOCATION,
                             PIPELINE,
                             PATH_PREFIX,
                             SCRIPT_LOCATION)

# probably shouldn't be using shell=True
cmd = subprocess.Popen(command, shell=True)
cmd.wait()

################################################################################
#                             start of tests                                   #
################################################################################

# check output to see if everything went ok
def test_loadddata():
    """generate_scripts creates loaddata file per plate"""
    loaddata_names = os.listdir(LOADDATA_LOCATION)
    assert len(loaddata_names) == 4


def test_loaddata2():
    """generate_scripts creates valid csv files for loaddata"""
    loaddata_names = os.listdir(LOADDATA_LOCATION)
    for f in loaddata_names:
        assert f.endswith(".csv")
    for f in loaddata_names:
        # create full file-paths
        full_path = os.path.abspath(f)
        tmp_df = pandas.read_csv(full_path)
        assert isinstance(tmp_df, pandas.DataFrame)


def test_we_have_scripts():
    """generate_scripts actually generates scripts"""
    script_names = os.listdir(SCRIPT_LOCATION)
    assert len(script_names) > 0


def test_scripts_are_ok():
    """generate_scripts that are not mangled"""
    pass


def test_scripts_command_inserted():
    """generate_scripts inserts cellprofiler command into template"""
    pass


def tearDown():
    """tidy up after testing"""
    to_remove = [LOADDATA_LOCATION, SCRIPT_LOCATION]
    map(shutil.rmtree, to_remove)
