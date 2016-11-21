"""
Class to create LoadData csv files from an ImageXpress experiment directory
"""

import json
import pandas as pd
# TODO sort out parse_path functions for extracting metadata from filenames
import parse_paths as pp
import os

class ImageList(object):
    """
    Create image lists from an ImageXpress experiment directory.
    ------------------------------------------------------------

    Example showing how to create a LoadData csv file per plate

        >> store = ImageList("/ImageExpress/2010-10-10/experiment_1")
        >> store.create_load_data()
        >> for name, data in store.load_data_files.items():
        >>     data.to_csv(name, index=False)
    """

    def __init__(self, exp_dir):
        self.exp_dir = exp_dir
        self.img_files = []
        self.plate_names = set()
        self.plate_img_store = dict()
        self.load_data_files = dict()


    def __len__(self):
        """number of plates"""
        return len(self.plate_names)


    def get_img_files(self, ext="tif"):
        """
        Given an ImageXpress experiment directory, this function will:
        - return a list of valid image paths for all plates in that experiment.
        - return a set of platenames
        """
        # TODO : speed this up! really slow.
        #        worse-case could call a find command in subprocess
        for root, _, files in os.walk(self.exp_dir):
            for f in files:
                if f.endswith(ext) and "thumb" not in f:
                    full_path = os.path.join(root, f)
                    self.img_files.append(full_path)
                    platename = full_path.split(os.sep)[-4]
                    self.plate_names.add(platename)


    def create_plate_img_store(self):
        """
        Create a dictionary:
        e.g {plate_name  : [list of img files],
             plate_name2 : [list of img files]}
        """
        # call get_img_files if it has not already been called
        if len(self.plate_names) == 0 or len(self.img_files) == 0:
            self.get_img_files()
        for plate in self.plate_names:
            # get only the image paths for a particular plate
            plate_img = [s for s in self.img_files if plate in s]
            # store in dictionary {plate : image_list}
            self.plate_img_store[plate] = plate_img


    def to_json(self, location):
        """
        store dictionary as JSON file

        Parameters:
        ------------
        location (string) :
            file path to save JSON file
        """
        with open(location, "wb") as save_point:
            json.dump(self.plate_img_store, save_point, indent=4)


    def from_json(self, location):
        """
        create plate : image_list dictionary from JSON dump

        Parameters:
        ------------
        location (string):
            file path of JSON file
        """
        with open(location, "r") as load_point:
            self.plate_img_store = json.load(load_point)


    def create_load_data(self):
        """
        parse metadata from file paths and convert into a dataframe suitable
        for CellProfiler's LoadData module
        """
        col_names = ["URL", "path", "Metadata_platename", "Metadata_well",
                     "Metadata_site", "Metadata_channel", "Metadata_platenum"]
        # create image list store if it hasn't already been called
        if len(self.plate_img_store) == 0:
            self.create_plate_img_store()
        # loop through dictionary of file-paths
        for plate, file_list in self.plate_img_store.items():
            filenames = pp.get_filename(file_list)
            pp.check_filename(filenames)
            df = pd.DataFrame(
                list(zip(
                    filenames,
                    pp.get_path(file_list),
                    pp.get_platename(file_list),
                    pp.get_metadata_well(file_list),
                    pp.get_metadata_site(file_list),
                    pp.get_metadata_channel(file_list),
                    pp.get_platenum(file_list)
                    ))
            )
            df.columns = col_names
            # reshape from long to wide format
            wide_df = self._cast_dataframe(df)
            self.load_data_files[plate] = wide_df


    def _cast_dataframe(self, dataframe):
        """
        reshape load_data_files dataframes from long to wide format
        """
        n_channels = len(set(dataframe.Metadata_channel))
        wide_df = dataframe.pivot_table(
            index=["Metadata_site", "Metadata_well", "Metadata_platenum",
                   "Metadata_platename", "path"],
            columns="Metadata_channel",
            values="URL",
            aggfunc="first").reset_index()
        # rename FileName columns from 1, 2... to FileName_W1, FileName_W2 ...
        columns = dict()
        for i in range(1, n_channels+1):
            columns[i] = "FileName_W" + str(i)
        wide_df.rename(columns=columns, inplace=True)
        # duplicate PathName for each channel
        for i in range(1, n_channels+1):
            wide_df["PathName_W" + str(i)] = wide_df.path
        wide_df.drop(["path"], axis=1, inplace=True)
        return wide_df
