# Useful stuff for running CellProfiler on Eddie3


## Batch processing
To batch run a CellProfiler analysis on an imageset, we need to split the images into multiple smaller jobs that can be run independently on the cluster.
To do this we can use `generate_scripts.py` to automatically generate the SGE submission scipts to analyse an experiment's images with a specified CellProfiler pipeline.

### Automatically generate submission scripts

```bash
./generate_scripts.py --experiment "path/to/experiment" \
                      --loaddata-location "/home/user/loaddata" \
                      --pipeline "/example/pipeline.cppipe" \
                      --path-prefix "/exports/eddie/scratch/user" \
                      --script-location "/home/user/submission_scripts"
```

This will save the submission scripts in `--script_location` or `-o`, with each job containing approximately 20 images each.  
The output from cellprofiler will be stored in the location given in `--path_prefix`, in a directory for each job named `path_prefix/platename_<JOB_NUMBER>`.

See `./generate_scripts --help` for more info.


### Generating batchlists

For a large numbers of jobs, it's often prefered to submit a single array job that references a list of cellprofiler commands, rather than substituting those cellprofiler commands into individual submission scripts. Therefore we can create a file that just contains a cellprofiler command on each line (a `batchlist`), that we can run using an array-job on the cluster.

```bash
./generate_batchlist.py --experiment "path/to/experiment" \
                        --loaddata-location "/home/user/loaddata" \
                        --pipeline "/example/pipeline.cppipe" \
                        --path-prefix "/exports/eddie/scratch/user"
```

We can can then use a single submission script run as an array-job to run all the cellprofiler commands - which stops angry emails from the cluster admins.


e.g to run 10,000 cellprofiler commands from `/exports/user/batchlist.txt`
```bash
#!/bin/bash
#$ -l h_vmem=6G
#$ -l h_rt=03:00:00
#$ -j y
#$ -o /exports/user/scratch
#$ -t 1-10000

. /etc/profile.d/modules.sh

module load igmm/apps/hdf5/1.8.16
module load igmm/apps/python/2.7.10
module load igmm/apps/jdk/1.8.0_66
module load igmm/libs/libpng/1.6.18

source /exports/igmm/eddie/Drug-Discovery/virtualenv-1.10/myVE/bin/activate
source ~/.bash_profile

SEEDFILE=/exports/user/batchlist.txt
SEED=$(awk "NR==$SGE_TASK_ID" $SEEDFILE)

$SEED

```


### Manually creating submission scripts via `ImageList`.

You can generate the submission scripts via the `ImageList` class in python.

Example:

```python
from create_image_list import ImageList

store = ImageList("/path/to/ImageXpress/experiment")
store.create_loaddata()
store.to_csv("/path/to/save/location")
```
This will generate .csv files suitable for CellProfilers LoadData module. It will create a .csv file per plate in the experiment directory.


```python
store.create_batchlist(pipeline="/path/to/pipeline.cppipe",
                       path_prefix="/exports/eddie/s0000")

store.batch_insert(template="/path/to/template/script",
                   location="/path/to/store/submission_scripts")
```

--------------------------------------------

## Merging the output

After running cellprofiler on the cluster you will have multiple .csv files, with the number dictated by how large your image list is and how many jobs you split it into.

To merge the csv files into a single file use `merge_output`, which takes a directory containing all the output as an argument and creates a single merged .csv file.

e.g
```sh
python merge_output.py "/path/to/directory"
```
This saves the resulting .csv file in the current working directory. To save it elsewhere pass an additional command line argument:
```sh
python merge_output.py "/path/to/directory" "/path/to/save/location"
```

#### Merging to a database

**Creating a database of results**

If there is a lot of data, then the sensible option is to create a database of the results. We can use `merge_to_db.py` to scan through multiple sub-directories and build an sqlite database from the .csv files.

If we have a directory of results containing multiple sub-folders, e.g:

```
results/
├── output_1
│   ├── DATA.csv
│   └── IMAGE.csv
├── output_2
│   ├── DATA.csv
│   └── IMAGE.csv
└── output_3
    ├── DATA.csv
    └── IMAGE.csv
```

```python
merger = ResultsDirectory("/results")
```

We then want to tell merge_to_db where to store the database.

```python
merger.create_db("/path/to/db/location")
```

Now we want the database to create separate tables for  `DATA` and `IMAGE`. We can specify the name of the .csv file we want to store in each table.

```python
merger.to_db("DATA")
merger.to_db("IMAGE")
```

This will automatically scan through the sub-directories, and read in the DATA and IMAGE files respectivley, appending each to the appropriate table.


**Multi-indexed columns**

CellProfiler can combine the results of different objects into a single csv file, when this is done it produces a .csv file with multi-indexed columns.

`merge_to_db` can automatically flatten these column headers before storing in the database if we specify the number of headers beforehand. So if `DATA` has two indices:

```python
merger.to_db("DATA", header=[0,1])
```


**Aggregating object-level data**

As the default output from CellProfiler is cell-level data, whereby we have a row per object, it's normally convenient to aggregate this to image or well averages. We can do this automatically when appending the raw-data to the database with the method `to_db_agg()`, which produces a separate table in the database named `<object>_agg`, where object is the name of the .csv file containing the raw data.

usage:

```python
merger.to_db_agg(select="DATA", header=[0,1], by="ImageNumber")
```

This will group the data by ImageNumber and create a row with a median value for each image.

We can change the aggregation function by passing the `agg_func` argument.

```python
merger.to_db_agg(select="DATA", header=[0,1], by="ImageNumber", agg_func="mean")
```

This will create a table called `DATA_agg` in the database, with a row per image.
