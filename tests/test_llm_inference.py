import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.llm_inference import load_model, clean_response, generate_response

MODEL_NAME = "deepseek-r1:8b"


@pytest.fixture(scope="module")
def setup_model():
    """Load the model once before running tests."""
    return load_model(MODEL_NAME)


def test_generate_response(setup_model):
    """Test LLM response generation with a sample prompt."""
    prompt = "Testing if LLM receives msg"

    try:
        generated_response = generate_response(MODEL_NAME, prompt)

        assert generated_response is not None, "LLM response is None"
        assert isinstance(generated_response, str), "Response should be a string"
        assert len(generated_response.strip()) > 0, "Response is empty"

    except Exception as e:
        pytest.fail(f"LLM inference test failed with error: {e}")
