#! /usr/bin/env python

import argparse
from create_image_list import ImageList

parser = argparse.ArgumentParser()

parser.add_argument("-e", "--experiment", type=str,
                    help="Experiment directory. The top level directory in the \
ImageExpress folder that contains plates as sub-directories.")

parser.add_argument("-l", "--loaddata-location", type=str,
                    help="Location to store LoadData files. These locations \
will be used in the SGE submission scripts for the LoadData module, so this \
location should have good IO performance")

parser.add_argument("-p", "--pipeline", type=str,
                    help="Path to cellprofiler pipeline.")

parser.add_argument("-r", "--path-prefix", type=str,
                    help="Prefix for results location. This is where the output \
will be saved. This needs to be somewhere with large amounts of space and good \
write performance - the user's scratch space is recommended")

parser.add_argument("-o", "--output-location", type=str,
                    help="Output location of the cellprofiler commands")

arguments = parser.parse_args()

if __name__ == "__main__":
    # generate the batch list
    store = ImageList(arguments.experiment)
    store.create_loaddata()
    store.to_csv(location=arguments.loaddata_location)
    store.create_batchlist(pipeline=arguments.pipeline,
                           path_prefix=arguments.path_prefix)
    store.save_batchlist(location=arguments.output_location)
