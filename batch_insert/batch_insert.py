#! /bin/env python

def write_batch_scripts(template, placeholder, batch_file):

    """
    converts a template qub submission script and a batch output file produced
    by cellprofiler to multiple consecutively numbered submission scripts
    arguments:
    ----------
    template   -- template submission script for qsub
    placehoder -- placeholder string within the template file. This will be
                  substituted with the cellprofiler command
    batch_file -- file produced by cellprofiler --get-batch-commands
    """

    tmp = open(template).read()
    inputs = open(batch_file).readlines()

    for i, cmd in enumerate(inputs, 1):
        out = tmp.replace(placeholder, cmd)
        outfile = open("out_{}".format(i), "w")
        outfile.write(out)


if __name__ == "__main__":
    write_batch_scripts(template="test_cp_batch_run.sh",
                        placeholder="PLACEHOLDER",
                        batch_file="batch_out.txt")