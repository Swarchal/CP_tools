#! /bin/sh

file="$1"
find "$file" -type f | grep -v "thumb\|.db"