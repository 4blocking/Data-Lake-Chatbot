import ollama
import re


def load_model(model_name):
    print(f"Loading model: {model_name}")
    return model_name


def clean_response(response_text):
    return re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()


def generate_response(model, prompt):
    """
    Generate a response from the LLM based on the given prompt.

    Args:
        model (str): Name of the LLM model.
        prompt (str): Prompt to send to the LLM.

    Returns:
        str: Cleaned response from the LLM.
    """
    response = ollama.chat(model=model, messages=[
        {"role": "system", "content": "You are an assistant trained on HDFS data. Your goal is to identify the data sources that match the query criteria."},
        {"role": "user", "content": prompt}
    ])

    cleaned_text = clean_response(response['message']['content'])
    return cleaned_text