import os
import pandas as pd
from sqlalchemy import create_engine

class ResultsDirectory:

    """
    Directory containing the .csv from a CellProfiler run
    ------------------------------------------------------
    - create_db(): creates an sqlite database in the results directory
    - to_db(): loads the csv files in the directory and writes them as
               tables to the sqlite database created by create_db()
    - truncate: argument will name files from text between the last underscore
      and .csv. e.g 'date_plate_cell.csv' will return 'cell'
    """

    def __init__(self, directory):
        """Get full filepaths of all files in a directory, including sub-directories"""
        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                # currently only getting DATA.csv files
                if filename.endswith("DATA.csv"):
                    file_paths.append(filepath)
            self.file_paths = file_paths


    # create sqlite database
    def create_db(self, location, db_name="results"):
        self.engine = create_engine('sqlite:///%s/%s.sqlite' % (location, db_name))


    # write csv files to database
    # currently appending all to the same table
    def to_db(self):
        for x,_ in enumerate(self.file_paths):
            f = self.file_paths[x]
            tmp_file = pd.read_csv(f, iterator=True, chunksize=1000)
            all_file = pd.concat(tmp_file)
            all_file.to_sql("DATA", con=self.engine,
                flavor ='sqlite', index=False, if_exists='append',
                chunksize=1000)

if __name__ == '__main__':
    x = ResultsDirectory("/home/scott/multi_index_test")
    x.create_db("/home/scott")
    x.to_db()