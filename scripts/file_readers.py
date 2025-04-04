# scripts/file_readers.py
from abc import ABC, abstractmethod
from scripts.spark_manager import get_spark_session
from pyspark.sql import functions as F

class FileReader(ABC):
    """Base class for file readers."""

    def __init__(self):
        self.spark = get_spark_session()

    @abstractmethod
    def read_file(self, hdfs_path, sample_size=5):
        """Read a file and return a sample of its content."""
        pass


class ParquetReader(FileReader):
    """Reader for Parquet files."""

    def read_file(self, hdfs_path, sample_size=5):
        try:
            df = self.spark.read.parquet(hdfs_path)
            sampled_rows = df.orderBy(F.rand()).limit(sample_size).toJSON().collect()
            return "\n".join(sampled_rows)
        except Exception as e:
            print(f"Error reading Parquet file: {e}")
            return None


class CSVReader(FileReader):
    def read_file(self, hdfs_path, sample_size=5):
        try:
            df = self.spark.read.csv(hdfs_path, header=True, inferSchema=False)
            header = ",".join(df.columns)

            sampled_rows = df.orderBy(F.rand()).limit(sample_size).collect()
            data = "\n".join([",".join(map(str, row)) for row in sampled_rows])
            return f"{header}\n{data}"
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

class JSONReader(FileReader):
    """Reader for JSON files."""
    def read_file(self, hdfs_path, sample_size=5):
        try:
            df = self.spark.read.json(hdfs_path)
            sampled_rows = df.orderBy(F.rand()).limit(sample_size).toJSON().collect()
            return "\n".join(sampled_rows)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return None

class TextReader(FileReader):
    """Reader for text files."""

    def read_file(self, hdfs_path, sample_size=5):
        try:
            df = self.spark.read.text(hdfs_path)
            sampled_rows = df.orderBy(F.rand()).limit(sample_size).collect()
            return "\n".join(row["value"] for row in sampled_rows)
        except Exception as e:
            print(f"Error reading text file: {e}")
            return None


class FileReaderFactory:
    """Factory to create file readers based on file extension."""

    @staticmethod
    def get_reader(hdfs_path):
        """Return the appropriate reader for the given file path."""
        if hdfs_path.endswith(".parquet"):
            return ParquetReader()
        elif hdfs_path.endswith(".csv"):
            return CSVReader()
        elif hdfs_path.endswith(".json"):
            return JSONReader()
        elif hdfs_path.endswith(".txt"):
            return TextReader()
        else:
            raise ValueError(f"Unsupported file format: {hdfs_path}")