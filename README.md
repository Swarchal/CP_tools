# Useful stuff for running CellProfiler on Eddie3

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

This will produce eddie submission scripts, having split the job into 20 image sets each, the cellprofiler jobs will save the output in `location`.

The jobs will access the LoadData csv files from the location specified in `ImageList.to_csv()`, so make sure it's somewhere worker nodes have acess to, and that it's somewhere efficient (i.e the scratch space).


### Automatically generate submission scripts

```python
./generate_scripts.py --experiment "path/to/experiment" \
                      --loaddata_location "/home/user/loaddata" \
                      --pipeline "/example/pipeline.cppipe" \
                      --path_prefix "/exports/eddie/scratch/user" \
                      --script_location "/home/user/submission_scripts"
```

Or, in shorthand:

```python
./generate_scripts.py -e "path/to/experiment" \
                      -l "/home/user/loaddata" \
                      -p "/example/pipeline.cppipe" \
                      -r "/exports/eddie/scratch/user" \
                      -o "/home/user/submission_scripts"

```

`./generate_scripts.py --help` for more info

### Merging the output

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
