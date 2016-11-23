"""
Test overall ImageList class on some example data to make sure I don't break
anything
"""

import sys
import os
import shutil

N_SITES_PLATE = 360
N_CHANNELS = 5
N_PLATES = 4
PATH_PREFIX = "/exports/eddie/user"
PIPELINE = "/example/pipeline.cppipe"


current_path = os.path.dirname(__file__)

def create_module_path():
    """need to import ImageList class from ../create_image_list.py"""
    module_path = os.path.realpath(os.path.join(current_path, ".."))
    sys.path.append(module_path)

create_module_path()
from create_image_list import ImageList

# get path to test directory
test_path = os.path.join(current_path, "example_dir")

store = ImageList(test_path)

store.create_loaddata()

# place to save test loaddata
loaddata_save_location = os.path.join(current_path, ".test_loaddata")
store.to_csv(loaddata_save_location)

store.create_batchlist(pipeline=PIPELINE,
                       path_prefix=PATH_PREFIX)


template_path = os.path.realpath(os.path.join(current_path, "..", "template_job.sh"))
qsub_script_location = os.path.join(current_path, ".test_submission_script")

store.batch_insert(template=template_path,
                   location=qsub_script_location)


def test_load_data_correct_num_plates():
    """correct number of plates"""
    assert len(store) == N_PLATES
    assert len(store.plate_names) == N_PLATES


def test_load_data_correct_images_plate():
    """correct number of images in each plate"""
    for img in store.plate_store.values():
        assert len(img) == N_SITES_PLATE * N_CHANNELS


def test_saved_to_csv():
    """load data files saved as csv"""
    assert len(os.listdir(loaddata_save_location)) == N_PLATES


def test_create_batch_list():
    """batch list created ok"""
    assert len(store.batch_list) == N_PLATES
    batch_start = "cellprofiler -r -c -p {}".format(PIPELINE)
    batch_end_0 = "-o {}/test-plate-1_1".format(PATH_PREFIX)
    batch_end_1 = "-o {}/test-plate-1_2".format(PATH_PREFIX)
    assert store.batch_list["test-plate-1"][0].startswith(batch_start)
    assert store.batch_list["test-plate-1"][0].endswith(batch_end_0)
    assert store.batch_list["test-plate-1"][1].endswith(batch_end_1)


def test_batch_insert():
    """insert commands into template script"""
    assert os.path.isdir(qsub_script_location)
    assert len(os.listdir(qsub_script_location)) > 0


def tearDown():
    """tidy up after testing"""
    shutil.rmtree(qsub_script_location)
    shutil.rmtree(loaddata_save_location)
