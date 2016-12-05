"""
Class to create LoadData csv files from an ImageXpress experiment directory
"""

from create_batch_list import create_batch_list
from batch_insert import write_batch_script
import json
import pandas as pd
import parse_paths as pp
import os

class ImageList(object):
    """
    Create image lists from an ImageXpress experiment directory.
    ------------------------------------------------------------

    Example showing how to create a LoadData csv file per plate:

        >>> store = ImageList("/ImageExpress/2010-10-10/experiment_1")
        >>> store.create_load_data()
        >>> store.to_csv("/home/swarchal/data/experiment_1/load_data")

    To create and insert cellprofiler batch commands into a submission script:
        >>> store.create_batch_list(pipeine="/path/to/pipeline.cppipe")
        >>> store.batch_insert(template="/path/to/template.sh",
                               location="/path/to/ouput")
    """

    def __init__(self, exp_dir):
        self.exp_dir = exp_dir
        self.img_files = []
        self.plate_names = set()
        self.plate_store = dict()
        self.load_data_files = dict()
        self.load_data_location = dict()
        self.load_data_stored = False
        self.batch_list = dict()


    def __len__(self):
        """number of plates"""
        return len(self.plate_names)


    def get_img_files(self, ext="tif"):
        """
        Given an ImageXpress experiment directory, this function will:
        - return a list of valid image paths for all plates in that experiment.
        - return a set of platenames
        """
        # TODO : speed this up! really slow, and lots of inefficiencies
        #        worse-case could call a find command in subprocess
        for root, _, files in os.walk(self.exp_dir):
            for f in files:
                if f.endswith(ext) and "thumb" not in f:
                    full_path = os.path.join(root, f)
                    self.img_files.append(full_path)
                    # FIXME this doesn't need to be done per file, only per plate
                    platename = full_path.split(os.sep)[-4]
                    self.plate_names.add(platename)


    def create_platestore(self):
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
            self.plate_store[plate] = plate_img


    def remove_plates(self, plate_list, keep=False):
        """
        Remove plates from platestore.

        Parameters:
        -----------
        plate_list : list of strings
            list of plate names
        keep : boolean
            if False, then the plates in `plate_list` will be removed. If True,
            then the paltes in `plate_list` will be kept and all others removed
        """
        if keep is False:
            # remove plates in plate_list from dictionary
            for plate in plate_list:
                self.plate_store.pop(plate)
        if keep is True:
            # remove all EXCEPT the plates in plate_list
            all_plates = self.plate_store.keys()
            to_remove = list(set(all_plates) - set(plate_list))
            for plate in to_remove:
                self.plate_store.pop(plate)


    def to_json(self, location):
        """
        store dictionary as JSON file

        Parameters:
        ------------
        location (string) :
            file path to save JSON file
        """
        with open(location, "wb") as save_point:
            json.dump(self.plate_store, save_point, indent=4)


    def from_json(self, location):
        """
        create plate : image_list dictionary from JSON dump

        Parameters:
        ------------
        location (string):
            file path of JSON file
        """
        with open(location, "r") as load_point:
            self.plate_store = json.load(load_point)


    def create_loaddata(self):
        """
        parse metadata from file paths and convert into a dataframe suitable
        for CellProfiler's LoadData module
        """
        col_names = ["URL", "path", "Metadata_platename", "Metadata_well",
                     "Metadata_site", "Metadata_channel", "Metadata_platenum"]
        # create image list store if it hasn't already been called
        if len(self.plate_store) == 0:
            self.create_platestore()
        # loop through dictionary of file-paths
        for plate, file_list in self.plate_store.items():
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


    @staticmethod
    def _cast_dataframe(dataframe):
        """
        internal function.
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


    def to_csv(self, location):
        """
        store LoadData as csv files in specified location.
        Each plate will be saved separately as $(location)/$(platename).csv
        If location is not an existing directory, then this will create the
        directory if permissions allow.

        Parameters:
        ------------
        location (string):
            path to directory in which to store LoadData csv files
        """
        if len(self.load_data_files) == 0:
            raise AttributeError("no load data files found")
        try:
            os.makedirs(location)
        except OSError:
            if os.path.isdir(location):
                pass
            else:
                err_msg = "failed to create directory {}".format(location)
                raise RuntimeError(err_msg)
        for name, dataframe in self.load_data_files.items():
            save_path = os.path.join(location, name) + ".csv"
            dataframe.to_csv(save_path, index=False)
            self.load_data_location[name] = save_path
        self.load_data_stored = True


    def create_batchlist(self, pipeline, **kwargs):
        """
        Create a list of cellprofiler commands from a file-list and a pipeline.
        This will use the LoadData files generated per plate and store
        a list of cellprofiler commands in a dictionary, with an entry for each
        plate.

        Parameters:
        ------------
        pipeline (string):
            path to pipeline
        **kwargs :
            additional arguments to create_batch_list()
                - n_chunks (default = None)
                - chunk_size (default = 20)
                - output_prefix (default = None)
                - full_path (default = True)
                - path_prefix (default = "")
        """
        # create LoadData dataframes if create_loaddata() has not been called
        if len(self.load_data_files) == 0:
            self.create_loaddata()
        if self.load_data_stored is False:
            msg = "LoadData files have not yet been saved as csv"
            raise AttributeError(msg)
        # clear any existing batch_list
        self.batch_list = dict()
        for name, dataframe in self.load_data_files.items():
            load_data_location = self.load_data_location[name]
            self.batch_list[name] = create_batch_list(
                loaddata=dataframe, pipeline=pipeline,
                loaddata_path=load_data_location, **kwargs)


    def save_batchlist(self, location, name="batch_commands.txt",
                       combined=False):
        """
        output batch commands as a text files. Useful if submitting an array
        job rather than inserting into individual submission scripts.

        Parameters:
        ------------
        location : string
            Directory in which to save output
        name : string
            Name of file (only used when combined=True). If combined is False,
            then the individual files will be named after the plate they came
            from
        combined : boolean
            If True, will combine multiple plate's batch commands into a single
            text file. If False, then will save a text file per plate
        """
        try:
            os.makedirs(location)
        except OSError:
            if os.path.isdir(location):
                pass
            else:
                err_msg = "failed to create directory {}".format(location)
                raise RuntimeError(err_msg)
        if combined is True:
            # all plates in a single file
            nested = self.batch_list.values()
            # unlist list of lists
            batch_commands = [item for sublist in nested for item in sublist]
            with open(os.path.join(location, name),"w") as out_file:
                out_file.write("\n".join(batch_commands))
        elif combined is False:
            # file per plate
            for plate, batch_commands in self.batch_list.items():
                with open(os.path.join(location, plate), "w") as out_file:
                    out_file.write("\n".join(batch_commands))
        else:
            raise ValueError("combined needs to be a boolean")


    def batch_insert(self, template, location, placeholder="PLACEHOLDER"):
        """
        Insert cellprofiler commands into template SGE submission script.
        This will generate a submission script for each batch command.

        Parameters:
        -----------
        template (string):
            path to template submission script
        location (string):
            path to directory to save the submissions scripts
        placeholder (string) default = "PLACEHOLDER":
            placeholder string in the submission script that will be replaced
            by the cellprofiler command
        """
        # check we actually have some batch commands
        if len(self.batch_list) == 0:
            msg = "No batch commands found, have you called create_batch_list?"
            raise AttributeError(msg)
        try:
            os.makedirs(location)
        except OSError:
            if os.path.isdir(location):
                pass
            else:
                msg = "Failed to create directory {}".format(location)
                raise RuntimeError(msg)
        # loop through batch lists and write each one to a file
        for batch_cmds in self.batch_list.values():
            write_batch_script(template=template, batch_list=batch_cmds,
                               location=location, placeholder=placeholder)
