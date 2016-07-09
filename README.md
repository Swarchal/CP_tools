# Useful stuff for running CellProfiler on Eddie3

Geared towards ImageXpress file directories and SGE job submissions.

- **batch_insert** substitutes `--get-batch-commands` output into a qsub script
- **make_LoadData** creates a .csv file for the LoadData module from an ImageXpress file directory
- **batch_LoadData** splits a LoadData .csv file into multiple cellprofiler commands to run as separate processes. 