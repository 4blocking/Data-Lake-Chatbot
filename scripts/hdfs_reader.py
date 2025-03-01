# scripts/hdfs_reader.py
from scripts.spark_manager import get_spark_session, stop_spark_session
from scripts.file_readers import FileReaderFactory


def list_hdfs_files(hdfs_dir):
    """
    List all files in an HDFS directory.

    Args:
        hdfs_dir (str): Path to the HDFS directory.

    Returns:
        list: List of file paths in the directory.
    """
    spark = get_spark_session()
    try:
        fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(spark._jsc.hadoopConfiguration())
        status = fs.listStatus(spark._jvm.org.apache.hadoop.fs.Path(hdfs_dir))
        file_paths = [str(file.getPath()) for file in status if file.isFile()]
        return file_paths
    except Exception as e:
        print(f"Error listing HDFS files: {e}")
        return []


def read_hdfs_file(hdfs_path, sample_size=5):
    """
    Read an HDFS file and return a sample of its content.

    Args:
        hdfs_path (str): Path to the HDFS file.
        sample_size (int): Number of rows to sample.

    Returns:
        str: Sampled data as a string.
    """
    try:
        reader = FileReaderFactory.get_reader(hdfs_path)
        return reader.read_file(hdfs_path, sample_size)
    except ValueError as e:
        print(e)
        return None