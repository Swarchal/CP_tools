#! /bin/env python

def write_batch_scripts(template, placeholder, batch_file, prefix=None):

    """
    converts a template qub submission script and a batch output file produced
    by cellprofiler to multiple consecutively numbered submission scripts
    arguments:
    ----------
    template   -- template submission script for qsub
    placehoder -- placeholder string within the template file. This will be
                  substituted with the cellprofiler command
    batch_file -- file produced by cellprofiler --get-batch-commands
    prefix -- prefix for submission scripts, if None will generate an
              appropriate prefix from the batch_file input
    """

    tmp = open(template).read()
    inputs = open(batch_file).readlines()

    if prefix == None:
        # determine prefix from batch_file input
        spacer = [" "]
        names = spacer + [i.split()[-1] for i in inputs]

    for i, cmd in enumerate(inputs, 1):
        out = tmp.replace(placeholder, cmd)
        outfile = open(str(names[i]), "w")
        outfile.write(out)
# TODO test this!!

if __name__ == "__main__":
    write_batch_scripts(template="test_cp_batch_run.sh",
                        placeholder="PLACEHOLDER",
                        batch_file="batch_out.txt")
