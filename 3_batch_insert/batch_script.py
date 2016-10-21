#!/usr/bin/env python

from __future__ import print_function
import argparse
import batch_insert


parser = argparse.ArgumentParser(description="create submission scripts")
parser.add_argument("-t", "--template", required=True)
parser.add_argument("-p", "--placeholder")
parser.add_argument("-f", "--batch_file")

parser.set_defaults(placeholder="PLACEHOLDER")

args=parser.parse_args()

batch_insert.write_batch_scripts(template=str(args.template),
                                 placeholder=str(args.placeholder),
                                 batch_file=str(args.batch_file))
