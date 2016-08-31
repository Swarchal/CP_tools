import os

def count_lines(fname):
    """return the number of lines in a file"""
    with open(fname) as f:
        for i, l in enumerate(f, 1):
            pass
    return i


def create_batch_list(file_list, pipeline, n_chunks=None,
                      output_prefix="output", full_path=True, chunk_size=20):
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
        output_prefix - prefix for the output folder
    """
    n_imagesets = count_lines(file_list)
    if n_chunks != None and chunk_size != 20:
        print ValueError("Cannot specify both chunk_size and n_chunks")
    if n_chunks == None or 0:
        #split into chunks containing roughly 20 imagesets
        n_chunks = n_imagesets // chunk_size
    chunk_size = n_imagesets // n_chunks
    remainder = n_imagesets - (chunk_size * n_chunks)
    if full_path == False:
        # trim path to just file name
        file_list = file_list.split(os.sep)[-1]
    output = []
    for i, val in enumerate(range(0, n_chunks), 1):
        if i < n_chunks:
            x = "cellprofiler -r -c -p {} --data-file={} -f {} -l {} -o {}{}".format(
                pipeline,
                file_list,
                ((i-1) * chunk_size) + 1,
                chunk_size * i,
                output_prefix,
                i
            )
        else:
            x = "cellprofiler -r -c -p {} --data-file={} -f {} -l {} -o {}{}".format(
                pipeline,
                file_list,
                ((i-1) * chunk_size) + 1,
                chunk_size * i + remainder,
                output_prefix,
                i
            )
        output.append(x)
    assert len(output) == n_chunks
    return output


if __name__ == '__main__':
    # quick check
    out =  create_batch_list(
        file_list="/home/scott/Dropbox/CP_tools/make_LoadData/load_data_input.csv",
        pipeline="20160711_cp_test2.cppipe",
        n_chunks=20,
        output_prefix="/exports/eddie/scratch/s1027820/output_",
        full_path=False)

    with open("out_file.txt", "w") as f:
        for i in out:
            f.write(i + "\n")
