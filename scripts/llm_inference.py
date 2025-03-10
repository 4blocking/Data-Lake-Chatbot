import ollama
import re
from openai import OpenAI
import os
from pydantic import BaseModel
from typing import List

# Read API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: Missing OpenAI API Key. Set OPENAI_API_KEY as an environment variable.")
client = OpenAI(api_key=OPENAI_API_KEY)

class DataSource(BaseModel):
    path: str
    reason: str

class FilteredDataSources(BaseModel):
    sources: List[DataSource]


def generate_response(model, prompt):
    """
    Generate a response using OpenAI API with Structured Outputs.

    Args:
        model (str): The model name.
        prompt (str): The user's query.

    Returns:
        list[dict]: A structured JSON response with relevant data sources.
    """
    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": " You are an AI assistant trained on HDFS data. Identify the most relevant data sources."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format=FilteredDataSources,
        )

        return response.choices[0].message.parsed

    except Exception as e:
        return f"OpenAI API Error: {str(e)}"


"""
def load_model(model_name):
    print(f"Loading model: {model_name}")
    return model_name
"""

"""
def clean_response(response_text):
    return re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()
"""

"""
def generate_response(model, prompt):
    \"\"\"
    Generate a response from the LLM based on the given prompt.

    Args:
        model (str): Name of the LLM model.
        prompt (str): Prompt to send to the LLM.

    Returns:
        str: Cleaned response from the LLM.
    \"\"\"
    response = ollama.chat(model=model, messages=[
        {"role": "system", "content": "You are an AI assistant that returns structured JSON responses."},
        {"role": "user", "content": prompt}
    ])

    response_text = response['message']['content']

    # Force extraction of JSON format from response
    match = re.search(r'\[(.*?)\]', response_text, re.DOTALL)
    if match:
        return "[" + match.group(1) + "]"
    else:
        return "Error: Response did not match expected JSON format."
"""

