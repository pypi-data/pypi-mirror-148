import unittest
import pathlib
import numpy as np

# Get location of this file
__this_file__ = pathlib.Path(__file__)
__this_path__ = __this_file__.parent.resolve()

# Get path to input to test_data data
test_data_path = __this_path__.joinpath('test_data')
test_data_file = test_data_path.joinpath('test_database_2.tim')


class TestStringMethods(unittest.TestCase):

    @classmethod
    def buildUpClass(cls) -> None:
        # Runs once before all test_data
        print(' Perform setup of test_data environment')
        numpy_export_file = test_data_file.with_suffix('.npz')
        if numpy_export_file.is_file():
            # Cleanup temporary _file
            numpy_export_file.unlink()
            print(f' Cleanup completed of: {numpy_export_file.as_posix()} ')

    @classmethod
    def tearDownClass(cls) -> None:
        # Runs once after all test_data
        print(' Perform tear down/cleaning of test_data environment')
        numpy_export_file = test_data_file.with_suffix('.npz')
        if numpy_export_file.is_file():
            # Cleanup temporary _file
            numpy_export_file.unlink()
            print(f' Cleanup completed of: {numpy_export_file.as_posix()} ')

    def test_001_read_rpc_file(self):
        """
            Test reading of rpc data
        """
        from rpc_viewer.rpc_viewer import ViewRPC
        print(f' Reading data from file: \n\t{test_data_file.as_posix()}\n')

        # Instantiate instance
        data_object = ViewRPC(test_data_file, debug=True)
        data_object.print_channel_header_data()
        self.assertTrue(True)

    def test_002_view_rpc_file(self):
        """
            Test plotting of channel 4 data
        """
        from rpc_viewer.rpc_viewer import ViewRPC
        print(f' Reading data from file: \n\t{test_data_file.as_posix()}\n')

        # Instantiate instance
        data_object = ViewRPC(test_data_file, debug=True)
        data_object.plot_channel(4)

        self.assertTrue(True)

    def test_003_view_rpc_file(self):
        """
            Test reading of rpc data
        """
        from rpc_viewer.rpc_viewer import ViewRPC
        print(f' Reading data from file: \n\t{test_data_file.as_posix()}\n')

        # Instantiate instance
        data_object = ViewRPC(test_data_file, debug=True)
        data_object.visualize_data()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
