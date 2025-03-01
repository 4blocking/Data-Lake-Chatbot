from scripts.hdfs_reader import list_hdfs_files, read_hdfs_file


class DataSourceManager:
    """Manages HDFS data sources and their samples."""

    def __init__(self, hdfs_dir, sample_size=5):
        """
        Initialize the DataSourceManager.

        Args:
            hdfs_dir (str): Path to the HDFS directory containing data files.
            sample_size (int): Number of rows to sample from each file.
        """
        self.hdfs_dir = hdfs_dir
        self.sample_size = sample_size
        self.hdfs_paths = list_hdfs_files(hdfs_dir)
        self.data_samples = self._load_samples()

    def _load_samples(self):
        """Load samples for all HDFS paths."""
        samples = {}
        for path in self.hdfs_paths:
            sample = read_hdfs_file(path, self.sample_size)
            if sample:
                samples[path] = sample
        return samples

    def get_samples(self):
        """Get all data samples."""
        return self.data_samples

    def get_sample(self, path):
        """Get the sample for a specific HDFS path."""
        return self.data_samples.get(path, None)