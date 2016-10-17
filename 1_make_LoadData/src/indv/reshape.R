#!/usr/bin/env Rscript

argv <- commandArgs(trailingOnly = TRUE)

if (length(argv) != 2) {
    stop("need to supply two arguments")
}

# TODO re-write this in python

library(reshape2)

df <- read.csv(argv[1])

out <- dcast(df, path + Metadata_well + Metadata_site + Metadata_platename +
             Metadata_platenum ~ Metadata_channel, value.var = "URL")

# rename column path to Metadata_path
colnames(out)[grep("path", colnames(out))] <- "Metadata_path"

# get column names not beginning with Metadata_
not_meta <- setdiff(1:ncol(out), grep("Metadata_", colnames(out)))

# produce vector of filenames
# FileName_W1 .... FileName_W[number of channels]
filenames <- vector(length = length(not_meta))
for (i in 1:length(not_meta)) {
    filenames[i] <- paste0("FileName_W", i)
}

colnames(out)[not_meta] <- filenames

# make a column of path names for each channel (going to be the same but with
# different column headers)

# create column names
pathnames <- vector(length = length(not_meta))
for (i in 1:length(not_meta)) {
    pathnames[i] <- paste0("PathName_W", i)
}

for (col_name in pathnames) {
    out[, col_name] <- out$Metadata_path
}

out[["Metadata_path"]] <- NULL

write.csv(out, argv[2], row.names = FALSE)
