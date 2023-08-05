import argparse
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import sys
import textwrap
from typing import Optional

from rpc_reader.rpc_reader import ReadRPC


class ViewRPC(object):
    """
    Plot content of RPC III files using MatPlotLib

    Lukas Stockmann
    2022-04-24
    """

    def __init__(self, _file, debug=False):
        """

        :param _file: Path to a rpc file
        :param debug: Flag for extra debugging output
        """
        # The file the data is stored in
        self.file: Optional[pathlib.Path, str] = None
        # The measurement data array stored in the file
        self.data: Optional[np.arrray] = None
        # Time array corresponding to the measurement data
        self.time: Optional[np.arrray] = None
        # End time of measurement
        self.end_time: Optional[float] = None
        # Complete Header of RPC file
        self.headers: Optional[dict] = None
        # Header for the individual channels
        self.channels: Optional[dict] = None

        # Check received _file
        if not isinstance(_file, pathlib.Path):
            _file = pathlib.Path(_file)
        if not _file.is_file():
            sys.exit("ERROR: The PRC test_data data file is invalid")
        self.file = _file

        # Instantiate instance
        data_object = ReadRPC(self.file, debug=True)

        # Check if the rpc file has been stored as a compressed numpy file
        file_path_data = self.file.with_suffix('.npz')

        if file_path_data.is_file():
            # Import data from compressed numpy file
            data_object.import_npy_data_from_file()
        else:
            # Import data from rpc_file
            data_object.import_rpc_data_from_file()
            # Export data as compressed numpy file
            data_object.save_npy_data_to_file(overwrite=False)

        self.data = data_object.get_data()
        self.time, self.end_time = data_object.get_time()
        self.headers = data_object.get_headers()
        self.channels = data_object.get_channels()

        # Verify that the un-pickled data is of dict type
        if isinstance(self.channels, np.ndarray):
            self.channels = self.channels.tolist()
        if isinstance(self.headers, np.ndarray):
            self.headers = self.headers.tolist()

    def plot_channel(self, channel):
        try:
            channel_metadata = self.channels[channel]
        except KeyError:
            print(f' ERROR: Requested channel is not available: {channel}')
            return

        # Create a figure containing a single axes.
        fig, ax = plt.subplots()
        # Plot some data on the axes.
        ax.plot(self.time, self.data[:, channel])

        if 'Channel' in channel_metadata and 'Description' in channel_metadata:
            desc = f"{channel_metadata['Channel']} - {channel_metadata['Description']}"
            plt.suptitle(desc)

        if 'Units' in channel_metadata:
            desc = f"{channel_metadata['Units']}"
            plt.ylabel(desc)

        # Add time legend
        plt.xlabel('Time [s]')

        # Show plot
        plt.show()

    def print_channel_header_data(self):
        for _channel, data in self.channels.items():
            print(f' Channel: {_channel + 1}')
            for key, value in data.items():
                print(f' \t {key:20s} : {value}')


def main():

    def argparse_check_file(_file):
        """
        'Type' for argparse - checks that file exists
        """
        # If = is in the path, split and use the right side only
        if '=' in _file:
            _file = _file.split('=')[1]
        _file = pathlib.Path(_file)
        if not _file.is_file():
            # Argparse uses the ArgumentTypeError to give a rejection message like:
            # error: argument input: x does not exist
            raise argparse.ArgumentTypeError("{0} is not a valid file".format(_file.as_posix()))
        return _file

    # Set-up parsing of input arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''

             Description:
             -----------------------------------------------------------------------------------------------------------
             Application for reading PRC 3 data files into numpy arrays. In the command line version, the provided file
             is converted into a numpy .npz file. To load the data use the numpy.load module which will load the numpy
             data as a dictionary with the following keys:

                header   - Header data
                time     - Time array
                channels - Channel data
                data     - The actual measurement data

             Written by: Niklas Melin
             Syntax examples:
                rpc_reader my_data_file.rpc
             '''))

    parser.add_argument("input_path",
                        type=argparse_check_file,
                        metavar='INPUT_PATH',
                        help="Select file containing something important \
                              \n\t  /path/to/my/input/file.rpc")
    parser.add_argument("--debug", "--d",
                        action="store_true",
                        help="If debug is set, significant additional output is requested.\n")

    # Parse arguments into a dictionary
    cmd_line_args = vars(parser.parse_args())

    # Get arguments
    input_path = cmd_line_args['input_path']
    debug = cmd_line_args['debug']

    # Start batch process
    reader_object = ReadRPC(input_path, debug=debug)
    reader_object.import_rpc_data_from_file()
    reader_object.save_npy_data_to_file()


if __name__ == '__main__':
    main()
