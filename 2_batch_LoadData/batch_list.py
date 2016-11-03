#!/usr/bin/env python

from __future__ import print_function
import argparse
import create_batch_list

parser = argparse.ArgumentParser(description="create cellprofiler batch commands")
parser.add_argument("-f", "--file_list", required=True, help="path to .csv file for LoadData")
parser.add_argument("-p", "--pipeline", required=True, help="cellprofiler pipeline")
parser.add_argument("-c", "--n_chunks")
parser.add_argument("-s", "--chunk_size")
parser.add_argument("-o", "--output_prefix")
parser.add_argument("-r", "--path_prefix")
parser.add_argument("-q", "--full_path")

parser.set_defaults(chunk_size=int(20),
                    prefix=None,
                    full_path=True)

args = parser.parse_args()

out = create_batch_list.create_batch_list(file_list=str(args.file_list),
                                          pipeline=str(args.pipeline),
                                          chunk_size=int(args.chunk_size),
                                          output_prefix=args.output_prefix,
                                          path_prefix=args.path_prefix,
                                          full_path=bool(args.full_path))

print(*out, sep="\n")
