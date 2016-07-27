# merge output

Following a cellprofiler analysis and using batch_LoadData with ExportToSpreadsheet, we produce many .csv files that we want to merge together.

## Creating a database of results

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


### Multi-indexed columns

CellProfiler can combine the results of different objects into a single csv file, when this is done it produces a .csv file with multi-indexed columns.

`merge_to_db` can automatically flatten these column headers before storing in the database if we specify the number of headers beforehand. So if `DATA` has two indices:

```python
merger.to_db("DATA", header=[0,1])
```