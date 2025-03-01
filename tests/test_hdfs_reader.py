import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.hdfs_reader import list_hdfs_files, read_hdfs_file

HDFS_TEST_DIR = "hdfs://localhost:9000/user/sources"
HDFS_TEST_FILE = "hdfs://localhost:9000/user/sources/3.csv"

# @pytest.mark.skip(reason="Requires a running HDFS instance")
def test_list_hdfs_files():
    files = list_hdfs_files(HDFS_TEST_DIR)
    assert isinstance(files, list)
    assert len(files) > 0, "No files found in the test HDFS directory."
    assert HDFS_TEST_FILE in files , "The test HDFS file was not found."

# @pytest.mark.skip(reason="Requires a running HDFS instance")
def test_read_hdfs_file():
    """Test reading an HDFS file and ensuring sample data is returned."""
    sample_data = read_hdfs_file(HDFS_TEST_FILE, sample_size=5)

    assert sample_data is not None, "Failed to read data from HDFS file."
    assert isinstance(sample_data, str), "Expected a string output from read_hdfs_file."
    assert sample_data.count("\n") + 1 >= 5, "Not enough rows returned from HDFS file."
