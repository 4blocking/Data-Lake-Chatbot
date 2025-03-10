from pyspark.sql import SparkSession
import yaml

with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

HDFS_DEFAULT_FS = config["hdfs"]["defaultFS"]

# Singleton SparkSession instance
_spark = None


def get_spark_session():
    """Get or create a Spark session for HDFS access."""
    global _spark
    if _spark is None:
        _spark = SparkSession.builder \
            .appName("HDFS_Reader") \
            .config("spark.hadoop.fs.defaultFS", HDFS_DEFAULT_FS) \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()
    return _spark


def stop_spark_session():
    """Stop the Spark session."""
    global _spark
    if _spark is not None:
        _spark.stop()
        _spark = None