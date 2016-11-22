import os
import pandas as pd

def count_lines(fname):
    """return the number of lines in a file"""
    i = 0
    if isinstance(fname, pd.DataFrame):
        i = fname.shape[0]
    elif isinstance(fname, str):
        with open(fname) as f:
            for i, _ in enumerate(f, 1):
                pass
    return i


def create_batch_list(loaddata, pipeline, loaddata_path, n_chunks=None,
                      chunk_size=20, path_prefix="", platename=None):
    """
    Create a list of cellprofiler commands for batch analysis from a filelist
    and a pipeline.

    This will split the file list into roughly equal sized chunks with the -f
    and -l flags as well as sequentially numbered output locations.

    If no argument is passed to n_chunks, then the number of chunks will
    be calculated automatically so that each chunk contains approximately
    20 imagesets.

    params:
        file_list - path to csv file suitable for load_data
        pipeline - cellprofiler pipeline that contains a valid LoadData module
        n_chunks - number of processes to run in parallel
    """
    n_imagesets = count_lines(loaddata)
    if n_chunks != None and chunk_size != 20:
        print ValueError("Cannot specify both chunk_size and n_chunks")
    if n_chunks == None or 0:
        #split into chunks containing roughly 20 imagesets
        n_chunks = n_imagesets // chunk_size
    chunk_size = n_imagesets // n_chunks
    remainder = n_imagesets - (chunk_size * n_chunks)
    if platename is None:
        # extract platename between the final file name and the extension
        filename = loaddata_path.split(os.sep)[-1]
        platename, _ = os.path.splitext(filename)
    output = []
    # get extension
    for i, _ in enumerate(range(0, n_chunks), 1):
        if i < n_chunks:
            x = "cellprofiler -r -c -p {} --data-file={} -f {} -l {} -o {}_{}".format(
                pipeline,
                loaddata_path,
                ((i-1) * chunk_size) + 1,
                chunk_size * i,
                os.path.join(path_prefix, platename),
                i
            )
        else:
            x = "cellprofiler -r -c -p {} --data-file={} -f {} -l {} -o {}_{}".format(
                pipeline,
                loaddata_path,
                ((i-1) * chunk_size) + 1,
                chunk_size * i + remainder,
                os.path.join(path_prefix, platename),
                i
            )
        output.append(x)
    return output
