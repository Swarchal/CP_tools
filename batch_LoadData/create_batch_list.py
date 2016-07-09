def count_lines(fname):
    """return the number of lines in a file"""
    with open(fname) as f:
        for i, l in enumerate(f, 1):
            pass
    return i


def create_batch_list(file_list, pipeline, n_chunks=None,
                      output_prefix="output"):
    """
    Create a list of cellprofiler commands for batch analysis from a filelist
    and a pipeline.

    This will split the file list into roughly equal sized chunks with the -f
    and -l flags as well as sequentially numbered output locations.

    If no argument is passed to n_chunks, then the number of chunks will
    be calculated automatically so that each chunk contains approximately
    20 imagesets.

    params:
        file_list - csv file suitable for load_data
        pipeline - cellprofiler pipeline that contains a valid LoadData module
        n_chunks - number of processes to run in parallel
        output_prefix - prefix for the output folder
    """

    n_imagesets = count_lines(file_list)

    if n_chunks == None:
        #split into chunks containing roughly 20 imagesets
        n_chunks = n_imagesets / 20

    chunk_size = n_imagesets / n_chunks
    remainder = n_imagesets - (chunk_size * n_chunks)

    output = []
    for i, val in enumerate(range(0, n_chunks), 1):
        x = "cellprofiler -r -c -p {} --data_file={} -f {} -l {} -o {}{}".format(
            pipeline,
            file_list,
            ((i-1) * chunk_size) + 1,
            chunk_size * i,
            output_prefix,
            i
        )
        output.append(x)

    # TODO add remainder to final -l count

    return output


if __name__ == '__main__':

    # quick check
    out =  create_batch_list(
        "/home/scott/Dropbox/CP_tools/make_LoadData/load_data_input.csv",
        "pipeline.cppipe",
        200)

    for i in out:
        print i