"""
Test overall ImageList class on some example data to make sure I don't break
anything
"""

from nose.tools import raises
import sys
import os
import shutil

N_SITES_PLATE = 360
N_CHANNELS = 5
N_PLATES = 4
PATH_PREFIX = "/exports/eddie/user"
PIPELINE = "/example/pipeline.cppipe"
CURRENT_PATH = os.path.dirname(__file__)

def create_module_path():
    """need to import ImageList class from ../create_image_list.py"""
    module_path = os.path.realpath(os.path.join(CURRENT_PATH, ".."))
    sys.path.append(module_path)

create_module_path()
from create_image_list import ImageList

# get path to test directory
test_path = os.path.join(CURRENT_PATH, "example_dir")

store = ImageList(test_path)

store.create_loaddata()

# place to save test loaddata
loaddata_save_location = os.path.join(CURRENT_PATH, ".test_loaddata")
store.to_csv(loaddata_save_location)

batchlist_save_location_indv = os.path.join(CURRENT_PATH, ".test_batchlist_indv")
batchlist_save_location_combn = os.path.join(CURRENT_PATH, ".test_batchlist_combn")
batchlist_save_location_combn2 = os.path.join(CURRENT_PATH, ".test_batchlist_combn2")

store.create_batchlist(pipeline=PIPELINE,
                       path_prefix=PATH_PREFIX)


template_path = os.path.realpath(os.path.join(CURRENT_PATH, "..", "template_job.sh"))
qsub_script_location = os.path.join(CURRENT_PATH, ".test_submission_script")

store.batch_insert(template=template_path,
                   location=qsub_script_location)


def test_load_data_correct_num_plates():
    """create image list -> correct number of plates"""
    assert len(store) == N_PLATES
    assert len(store.plate_names) == N_PLATES


def test_load_data_correct_images_plate():
    """ create image list -> correct number of images in each plate"""
    for img in store.plate_store.values():
        assert len(img) == N_SITES_PLATE * N_CHANNELS


def test_saved_to_csv():
    """load data files saved as csv"""
    output = os.listdir(loaddata_save_location)
    assert len(output) == N_PLATES
    for i in output:
        assert i.endswith(".csv")
    assert len(set(output)) == len(output)


def test_create_batch_list():
    """batch list internal dict created ok"""
    assert len(store.batch_list) == N_PLATES

def test_create_batch_list2():
    """batch list internal dict contents ok"""
    batch_start = "cellprofiler -r -c -p {}".format(PIPELINE)
    batch_end_0 = "-o {}/test-plate-1_1".format(PATH_PREFIX)
    batch_end_1 = "-o {}/test-plate-1_2".format(PATH_PREFIX)
    assert store.batch_list["test-plate-1"][0].startswith(batch_start)
    assert store.batch_list["test-plate-1"][0].endswith(batch_end_0)
    assert store.batch_list["test-plate-1"][1].endswith(batch_end_1)


def test_save_batch_list_indv():
    """batch list saved individually"""
    store.save_batchlist(location=batchlist_save_location_indv, combined=False)
    assert len(os.listdir(batchlist_save_location_indv)) == N_PLATES


def test_save_batch_list_indv2():
    """batch list saved individually -> names are correct"""
    # check the files are named after the plates
    plate_names = ["test-plate-1", "test-plate-2",
                   "test-plate-3", "test-plate-4"]
    assert sorted(os.listdir(batchlist_save_location_indv)) == plate_names


def test_save_batch_list_indv3():
    """batch list saved indivually -> check contents are correct"""
    batch_start = "cellprofiler -r -c -p {}".format(PIPELINE)
    for plate in os.listdir(batchlist_save_location_indv):
        file_path = os.path.join(batchlist_save_location_indv, plate)
        with open(file_path, "r") as f:
            contents = [i.strip() for i in f.readlines()]
            for line in contents:
                assert line.startswith(batch_start)


def test_save_batchlist_combn():
    """batch list saved combined"""
    store.save_batchlist(location=batchlist_save_location_combn, combined=True)
    assert len(os.listdir(batchlist_save_location_combn)) == 1


def test_save_batch_list_combn2():
    """batch list save combined with name changed"""
    filename = "writing_tests_is_dull"
    store.save_batchlist(location=batchlist_save_location_combn2,
                         combined=True, name=filename)
    files = os.listdir(batchlist_save_location_combn2)
    print(files)
    assert len(files) == 1
    assert str(files[0]) == filename


def test_save_batch_list_combn3():
    """batch list saved combined -> check contents are correct"""
    batch_start = "cellprofiler -r -c -p {}".format(PIPELINE)
    file_path = os.path.join(batchlist_save_location_combn, "batch_commands.txt")
    contents = [i.strip() for i in open(file_path)]
    assert len(contents) > 20
    for line in contents:
        assert line.startswith(batch_start)


def test_batch_insert():
    """insert commands into template script"""
    assert os.path.isdir(qsub_script_location)
    assert len(os.listdir(qsub_script_location)) > 0


# all the way down here as these plates will be removed, and I can't be bothered
# to create the image list again
def test_remove_plates():
    """remove plates from plate_store"""
    store.remove_plates(["test-plate-1"])
    assert "test-plate-1" not in store.plate_names
    assert "test-plate-1" not in store.plate_store.keys()


def test_remove_plates2():
    """remove plates -> catch KeyErrors"""
    plates_to_remove = ["test-plate-2", "not a plate"]
    store.remove_plates(plates_to_remove, key_error=False)
    assert len(store.plate_names) == 2


@raises(KeyError)
def test_remove_plates3():
    """remove plates -> expect KeyError"""
    plates_to_remove = ["not here" "test-plate-3"]
    store.remove_plates(plates_to_remove, key_error=True)


def test_remove_plates4():
    """remove plates -> keep argument works"""
    plates_to_remove = ["test-plate-4"]
    store.remove_plates(plates_to_remove, keep=True)
    assert len(store.plate_names) == 1
    assert list(store.plate_names)[0] == plates_to_remove[0]



def tearDown():
    """tidy up after testing"""
    to_remove = [qsub_script_location,
                 loaddata_save_location,
                 batchlist_save_location_indv,
                 batchlist_save_location_combn,
                 batchlist_save_location_combn2]
    map(shutil.rmtree, to_remove)
