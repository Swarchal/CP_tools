#!/usr/bin/env python

import argparse
import os
from create_image_list import ImageList

parser = argparse.ArgumentParser()

parser.add_argument("-e", "--experiment", type=str,
                    help="experiment directory. The top level file in the\
ImageExpress folder that contains plates as sub-directories.")

parser.add_argument("-l", "--loaddata-location", type=str,
                    help="location to store LoadData files. These locations\
will be used in the SGE submission scripts for the LoadData module, so this\
location should have good IO performance")

parser.add_argument("-p", "--pipeline", type=str,
                    help="path to cellprofiler pipeline.")

parser.add_argument("-r", "--path-prefix", type=str,
                    help="prefix for results location. This is where the output\
will be saved. The user's scratch space is recommended")

parser.add_argument("-o", "--script-location", type=str,
                    help="location to save submission scripts. This is where\
SGE submission scripts will be saved to.")

arguments = parser.parse_args()


def main():
    store = ImageList(arguments.experiment)
    store.create_loaddata()
    store.to_csv(location=arguments.loaddata_location)
    store.create_batchlist(pipeline=arguments.pipeline,
                           path_prefix=arguments.path_prefix)
    # get path of template script
    path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(path, "template_job.sh")
    store.batch_insert(template=template_path,
                       location=arguments.script_location)

if __name__ == "__main__":
    main()
