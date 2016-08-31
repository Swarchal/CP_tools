## TODO

- [ ] re-write `make_LoadData/src/reshape.R` in python
- [x] ability to merge additional Metadata based on well and plate
- [ ] Have a metadata image URL so we have the possibility to link images to datapoints
- [ ] See if there are any quicker ways than using `find`, as this is quite slow for large directories
- Alter file paths for local and cluster paths
    - e.g at the moment it's `/mnt/ImageXpress/` locally, yet `/export/igmm/datastore/ImageExpress` on Eddie.
    - Can do this ad hoc with with `gsub` or `str.replace`, but would be nice to have it as an initial option.
- [ ] write some tests
- [x] `merge_output` option to save to database (sqlite)
