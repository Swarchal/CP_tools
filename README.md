# Useful stuff for running CellProfiler on Eddie3

Geared towards ImageXpress file directories and SGE job submissions.

- **batch_insert** substitutes `--get-batch-commands` output into a qsub script
- **make_LoadData** creates a .csv file for the LoadData module from an ImageXpress file directory
- **batch_LoadData** splits a LoadData .csv file into multiple cellprofiler commands to run as separate processes.

## Example


### 1. Create a suitable cellprofiler pipeline

Create a cellprofiler pipeline with a LoadData module at the beginning that takes a .csv file from `default input` or `elsewhere`. At the end of the pipeline have a ExportToSpreadsheet module, that saves the output at `default output` location. This output location can then be specified on the command line by the `-o` option.

### 2. Generate input for LoadData

Create a file list suitable for LoadData using `make_LoadData`, by `cd`'ing to the directory containing `filesnames.sh` and passing an argument containing the top directory of images you want to analyse. e.g

```
cd ~/CP_tools/make_LoadData
./filenames.sh /images/project_1
```

This generates a .csv file suitable for LoadData and automatically extracts metadata such as plate name, well name, site and channel number. The generated image list is saved in the `make_LoadData/` directory.

### 3. Generate submission commands

Whilst we can pass this image list to cellprofiler, it will analyse the images serially and take a long time. Ideally we want to run this in parallel, so we use `batch_LoadData` to split this image list up into equal sized chunks and farm these out to a computing cluster.

`batch_LoadData` generates a file containing the cellprofiler commands to run the image set in small discrete chunks, and save the ouput in sequentailly numbered output directories.

To run `batch_LoadData` we pass a file_list, a cellprofiler pipeline, and then arguments to either specify the number of chunks or roughly how many images should be in each chunk. If no chunk arguments are set then it will split the file list into chunks containing roughly 20 imagesets each.

```python
create_batch_list(file_list="~/data/load_data_input.csv"
                  pipeline="~/data/project_1.cppipe",
                  n_chunks=500,
                  output_prefix="/scratch/project_1_output_")
```

This creates a file containing 500 cellprofiler commands. e.g

```
cellprofiler -r -c -p ~/data/project_1.cppipe --data-file=~/data/load_data_input.csv -f 1 -l 10 -o /scratch/project_1_output_1
cellprofiler -r -c -p ~/data/project_1.cppipe --data-file=~/data/load_data_input.csv -f 11 -l 20 -o /scratch_/project_1_output_2
cellprofiler -r -c -p ~/data/project_1.cppipe --data-file=~/data/load_data_input.csv -f 21 -l 30 -o /scratch/project_1_output_3
...
```

Or alternatively, we can pass the chunk_size.

```python
create_batch_list(file_list="~/data/load_data_input.csv"
                  pipeline="~/data/project_1.cppipe",
                  chunk_size=30,
                  output_prefix="/scratch/project_1_output_")
```

### 4. Creating submission scripts

Now that we have a file containing all the cellprofiler commmands, we want to place these into individual submission scripts that can be submitted to the computing cluster. This is often necessary as cellprofiler requires multiple modules to be loaded before it can be run.

We can make a template submission script with everything required to run the job, except for the cellprofiler commands, which are substituted for a placeholder string.

e.g if we have a template file called `cp_run.sh`:

```sh
#!/bin/sh
#$ -l h_vmem=10G
#$ -cwd
#$ -l h_rt:10:00:00

# activate python virtual environment for dependencies
source /home/s1027820/virtualenv-1.10/myVE/bin/activate

# source bash profile for correct java paths
source /home/s1027820/.bash_profile

# cd to directory containing images and pipeline
cd /exports/eddie/scratch/s1027820/test_2

# cellprofiler command
PLACEHOLDER
```

And a file from `create_batch_list` called `batch_out.txt`

We can then generate a submission script for each command using:

```python
write_batch_scripts(template="cp_run.sh",
                    placeholder="PLACEHOLDER",
                    batch_file="batch_out.txt")
```

This will generate a sequentially numbered qsub script name `out_1` ... `out_n`.

### 5. Submitting the jobs to the cluster

This can be done with a bash loop.

```sh
for i in {1..200}; do qsub out_$i; done
```