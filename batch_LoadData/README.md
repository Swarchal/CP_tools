# Create batch submission from LoadData and pipeline

> "Batch Nah!"

Idea is to use LoadData and the pipeline rather than BatchFiles. This script will take a LoadData .csv files and a pipeline as input and split into a specified number of chunks and generate the cellprofiler commands to farm out to run on a cluster.

This requires splitting the LoadData csv file into roughly equal sized chunks and sending the output to sequentially numbered output folders.
