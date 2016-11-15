import os
import sys

def _count_lines(in_file):
    """Number of lines in a file"""
    with open(in_file) as f:
        return sum(1 for _ in f)


def n_file_lists(file_list_dir, n):
    """Check we have the expected number of file lists"""
    files = os.listdir(file_list_dir)
    return len(files) == n


def len_file_lists(file_list_dir, expected_len):
    """Check the file lists are the expected length"""
    file_lists = os.listdir(file_list_dir)
    # need to count the number of lines in the file and subtract 1 (header line)
    for f in file_lists:
        # bit of a dodgy way to do it
        # create abs file path
        f_path = os.path.join(os.path.abspath(file_list_dir), f)
        if _count_lines(f_path) != expected_len:
            return False
        else:
            return True


def n_batch_commands(batch_cmd_dir, n_expected_commands):
    """Check we have the expected number of batch commands"""
    file_list = os.listdir(file_list_dir)
    for f in file_list:
        if _count_lines(os.path.abspath(f)) != n_expected_commands:
            return False
        else:
            return True


def _check_contents(x, scratch_location="/exports/eddie/scratch/s1027820"):
    """
    check contents of batch line
    NOTE this will fail if there are unescaped spaces in file paths
    """
    contents = x.split()
    if contents[0] != "cellprofiler" and "Cellprofiler":
        return False
    if contents[1] != "-r":
        return False
    if contents[2] != "-c":
        return False
    if contents[3] != "-p":
        return False
    if not contents[4].startswith("--data-file="):
        return False
    if contents[5] != "-f":
        return False
    # try and convert file number into integer
    try:
        int(contents[6])
    except:
        return False
    if contents[7] != "-l":
        return False
    try:
        int(contents[8])
    except:
        return False
    if int(contents[6]) > int(contents[8]):
        return False
    if contents[9] != "-o":
        return False
    if not contents[10].startswith(scratch_location):
        return False
    # if nothing bad happens up util here:
    return True


def typical_batch_command(batch_command_dir, **kwargs):
    """Check the batch commands are properly formed"""
    file_list = os.listdir(batch_command_dir)
    for f in file_list:
        f_path = os.path.join(os.path.abspath(batch_command_dir), f)
        for line in open(f_path).readlines():
            ans = _check_contents(line, **kwargs)
            if ans == True:
                continue
            else:
                return False
    return True


def n_submission_scripts(sub_dir, n):
    """Check there is at least one submission script per plate"""
    submission_list = os.listdir(sub_dir)
    return len(submission_test) == n


def _compare_with_template(script_path, template_path):
    """check the submission script has been substituted"""
    with open(template_path) as template:
        with open(script_path) as script:
            template_o = template.readlines()
            script_o = script.readlines()
            # compare lines, count number of differences
            # should only be one (substituting the placeholder)
            for i in range(len(template_o)):
                diff = 0
                if template_o[i] != script_o[i]:
                    diff += 1
            if diff != 1:
                return False
            else:
                return True


def check_submission_script(sub_dir, template_path):
    """Check it's a properly formed eddie submission script"""
    submission_scripts = os.listdir(sub_dir)
    for f in submission_scripts:
        f_path = os.path.join(os.path.abspath(sub_dir), f)
        ans = _compare_with_template(f_path, template_path)
        if ans == True:
            continue
        else:
            return False
    return True
