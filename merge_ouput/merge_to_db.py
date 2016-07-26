import os
import pandas as pd
import colfuncs
from sqlalchemy import create_engine

class ResultsDirectory:


    """
    Directory containing the .csv from a CellProfiler run
    ------------------------------------------------------
    - create_db(): creates an sqlite database in the results directory
    - to_db(): loads the csv files in the directory and writes them as
               tables to the sqlite database created by create_db()
    """

    def __init__(self, directory):
        """
        Get full filepaths of all files in a directory, including sub-directories
        """
        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
            self.file_paths = file_paths


    # create sqlite database
    def create_db(self, location, db_name="results"):
        self.engine = create_engine("sqlite:///%s/%s.sqlite" % (location, db_name))


    # write csv files to database
    def to_db(self, select="DATA", header=[0,1]):
        """
        select: the name of the .csv file, this will also be the database table
        header: the number of header rows.
                N.B. if not multi-indexed then use 0 rather than [0].
        """
        # filter files
        file_paths = [f for f in self.file_paths if f.endswith(select+".csv")]

        for x, _ in enumerate(file_paths):
            f = file_paths[x]
            tmp_file = pd.read_csv(f, header=header, iterator=True)
            all_file = pd.concat(tmp_file) # collect iterator

            # collapse column names if multi-indexed
            if isinstance(all_file.columns, pd.core.index.MultiIndex):
                all_file.columns = colfuncs.collapse_cols(all_file)

            all_file.to_sql(select, con=self.engine,
                flavor ="sqlite", index=False, if_exists="append")

if __name__ == '__main__':
    x = ResultsDirectory("/home/scott/multi_index_test")
    x.create_db("/home/scott")
    x.to_db(select="DATA", header=[0,1])
    x.to_db(select="IMAGE", header=0)