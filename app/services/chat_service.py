from scripts.hdfs_reader import read_hdfs_file
from scripts.llm_inference import generate_response
from scripts.data_source_manager import DataSourceManager
import yaml
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the current file
CONFIG_PATH = os.path.join(BASE_DIR, "..", "..", "config", "config.yaml")  # Navigate to the root directory

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)


HDFS_DIR = config["hdfs"]["base_dir"]
SAMPLE_SIZE = config["hdfs"]["sample_size"]
MODEL_NAME = config["llm"]["model_name"]


def process_chat_query(query: str) -> str:
    """Processes a user query by fetching sample data and querying the LLM."""

    # Initialize DataSourceManager to get hdfs samples
    data_manager = DataSourceManager(HDFS_DIR, SAMPLE_SIZE)
    data_samples = data_manager.get_samples()

    if not data_samples:
        return "No data sources found in HDFS.Ensure HDFS is running and your path is correct."

    prompt = build_prompt(query, data_samples)
    response = generate_response(MODEL_NAME, prompt)

    return response


def build_prompt(query, data_samples):
    """Builds a prompt for the LLM based on user query and HDFS data."""
    prompt = f"""
    Analyze the following HDFS data samples and identify which data sources contain information related to: '{query}'.
    Provide the exact path and a very brief explanation of its relevance.
    For each relevant data source, provide:
    1. The exact path to the data source.
    2. A very brief explanation of why it is relevant to the query.

    Data Sources:
    """

    for path, sample in data_samples.items():
        prompt += f"\nPath: {path}\nSample:\n{sample}\n"

    prompt += "\nAnswer with relevant paths and explanations:"
    return prompt
