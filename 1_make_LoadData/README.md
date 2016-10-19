# Scripts for creating LoadData input

The `filenames.sh` script will generate a .csv file for CellProfiler's LoadData module when given a top level directory in an ImageXpress directory.

## usage:

1. cd to the directory containing `filenames.sh`
2. Run `./filenames.sh path/to/folder`
3. This produces a `load_data_input.csv` file in the same directory as `filenames.sh`.

### adding metadata:

Passing an additional metadata .csv file to `./filenames.sh` will merge metadata to the appropriate well and plate labels

```bash
./filenames.sh /path/to/folder metadata_file.csv
```

The metadata file should contain well labels under the columns `Metadata_well` and optionally, a column of `Metadata_platename`.


## Creating a LoadData file for each plate
```bash
./create_load_data.sh /path/to/plates /path/to/save
```

This will create a csv for load data for every plate in the `path/to/plates` directory.

This is useful for screens containing a large number of plates, and easily re-running analyses for certain plates.
