import os

def write_batch_script(template, placeholder, batch_list, location=None):

    """
    converts a template qub submission script and a batch output file produced
    by cellprofiler to multiple consecutively numbered submission scripts
    arguments:
    ----------
    template   -- template submission script for qsub
    placehoder -- placeholder string within the template file. This will be
                  substituted with the cellprofiler command
    batch_list --
    """
    # if no location given, then just save without prefix
    if location is None:
        location = ""
    tmp = open(template).read()
    for cmd in batch_list:
        names = cmd.split()[-1].split(os.sep)[-1]
        out = tmp.replace(placeholder, cmd)
        path = os.path.join(location, names)
        outfile = open(path, "w")
        outfile.write(out)
        outfile.close()
