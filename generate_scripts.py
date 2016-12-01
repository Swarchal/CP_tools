#!/usr/bin/env python

import argparse
import os
from create_image_list import ImageList

parser = argparse.ArgumentParser()

parser.add_argument("-e", "--experiment", type=str,
                    help="experiment directory")

parser.add_argument("-l", "--loaddata-location", type=str,
                    help="location to store LoadData files")

parser.add_argument("-p", "--pipeline", type=str,
                    help="path to cellprofiler pipeline")

parser.add_argument("-r", "--path-prefix", type=str,
                    help="prefix for results location")

parser.add_argument("-o", "--script-location", type=str,
                    help="location to save submission scripts")

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
