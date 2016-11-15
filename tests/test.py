#!/usr/bin/env python

"""
Test of main.sh using the example directory. This contains empty files with
typical ImageXpress names.
"""

from colors import bcolors as col
import os
import shutil
import sys
import subprocess
import test_funcs as test
import time

N_TEST_PLATES = 4
N_IMAGES_PER_PLATE = 360

# clear the temporary directories before running
# if files contained within the temporary directories (or just submission_scripts)
# then warn the user, and ask if they want to continue
dirs_to_remove = ["../file_lists",
                  "../batch_commands",
                  "../submission_scripts"]

for directory in dirs_to_remove:
    if os.path.isdir(directory):
        if os.listdir(directory) != []: # if directory is not empty
            print("Files found in {}, these will be deleted".format(directory))
            print("Do you want to continue? (y/[n])")
            if sys.version_info > (3, 0):
                ans = input()
            else:
                ans = raw_input()

            if ans.lower() == "y":
                shutil.rmtree(directory)
            elif ans.lower() == "n":
                sys.exit()

print("\nCreating submission scripts...")

# change directory so can call main.sh directly, otherwise the file-paths
# are all wrong.
# TODO Should probably fix that in main.sh to use more robust file paths
#      as it seems to pick up the filepath from where main was called rather
#      than using the location of main.sh

# bodge ahoy!
os.chdir("..")
cwd = os.getcwd()

# run command
bash_command = "./main.sh -f {}/tests/example_dir \
                -p example_pipeline.cppipe \
                -s /exports/eddie/scratch/s1027820".format(cwd)
process = subprocess.Popen(bash_command, shell=True)
# wait for process to finish, otherwise python is too eager and looks for
# directories that don't yet exist
process.wait()


print("\nRunning tests on output...")

# check we've created a a file-list for each plate
file_list_path = os.path.abspath("file_lists")
file_list_len = test.len_file_lists(file_list_path,
                                      expected_len=N_IMAGES_PER_PLATE + 1)
print("Expected length of file lists : {}{}{}".format(col.BOLD,
                                                      file_list_len,
                                                      col.ENDC))

# check we've created a list of batch commands for each plate
file_list_count = test.n_file_lists(file_list_path, n=N_TEST_PLATES)
print("Expected number of file lists : {}{}{}".format(col.BOLD, file_list_count,
                                                      col.ENDC))


# TODO check we have the correct number of batch commands
# NOTE this depends on how the split the image set up

# now we need to check it's created the submission scripts
batch_path = os.path.abspath("batch_commands")
batch_ans = test.typical_batch_command(batch_path)
print("Correctly formatted batch commands : {}{}{}".format(col.BOLD,
                                                           batch_ans,
                                                           col.ENDC))

# TODO check we have at least one submission script per plate


# TODO check the submission scripts are correct
submission_path = os.path.abspath("submission_scripts")
template_path = os.path.abspath("template_job.sh")
sub_ans = test.check_submission_script(submission_path, template_path)
print("Correctly formed submission script : {}{}{}".format(col.BOLD,
                                                           sub_ans,
                                                           col.ENDC))

# check if any were False
test_ans = [file_list_count, batch_ans, sub_ans]
overall_ans = sum(test_ans) == len(test_ans)

if overall_ans == True:
    print("\nTEST : {}PASS{}".format(col.OKGREEN, col.ENDC))
if overall_ans == False:
    print("\nTEST : {}FAIL{}".format(col.FAIL, col.ENDC))