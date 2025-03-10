from scripts.llm_inference import generate_response
from scripts.data_source_manager import DataSourceManager
from scripts.hive_manager import read_metadata
import yaml
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the current file
CONFIG_PATH = os.path.join(BASE_DIR, "..", "..", "config", "config.yaml")  # Navigate to the root directory

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)


HDFS_DIR = config["hdfs"]["base_dir"]
SAMPLE_SIZE = config["hdfs"]["sample_size"]
MODEL_NAME = config["llm"]["model_name"]


def process_chat_query(query: str) -> str | list[dict]:
    """Processes a user query by fetching sample data and querying the LLM."""

    # Initialize DataSourceManager to get hdfs samples
    data_manager = DataSourceManager(HDFS_DIR, SAMPLE_SIZE)
    data_samples = data_manager.get_samples()

    metadata = read_metadata()

    if not data_samples and not metadata:
        return "No data sources found in HDFS or Hive .Ensure HDFS or Hive is running and your path is correct."

    prompt = build_prompt(query, data_samples,metadata)
    response = generate_response(MODEL_NAME, prompt)

    return response


def build_prompt(query, data_samples, metadata):
    """Builds a structured prompt for the LLM with strict filtering instructions."""
    prompt = f"""
        You are an AI assistant trained to analyze data sources.
        Identify the **most relevant** data sources based on the user's query.

        **Query:** "{query}"

        **Rules:**
        - **Only return relevant sources.**
        - **Do NOT summarize unrelated datasets.**
        - **Return an empty list `[]` if no sources match.**

        ### **Hive Metadata:**
        """
    for row in metadata:
        prompt += f"\n- **Path:** {row[0]}\n**Format:** {row[1]}\n**Description:** {row[2]}\n**Domain:** {row[3]}\n**Keywords:** {row[4]}\n"

    if data_samples:
        prompt += "\n### **Data sources samples:**"
        for path, sample in data_samples.items():
            prompt += f"\n- **Path:** {path}\n**Sample:**\n{sample}\n"


    prompt += "\n**Return only the relevant data sources in the exact JSON format. If nothing matches, return `[]`**."
    print(prompt)
    estimated_tokens = len(prompt)/3
    print(estimated_tokens)
    return prompt


