# merge output

Following a cellprofiler analysis and using batch_LoadData with ExportToSpreadsheet, we produce many .csv files that we want to merge together.

`merge_output`, if given a directory containing the cellprofiler ouput will read in the csv files and produce a single file.

:warning: This is assuming we have multi-indexed columns for combined object data in cellprofiler.