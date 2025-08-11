import ollama
from ollama import chat, ChatResponse
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import coverage
import io
import sys
import pytest
import re

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)
client = OpenAI(api_key = OPENAI_API_KEY)

# % Coverage we want
TARGET_COVERAGE = 90

# % Tests passed we want
TARGET_ACCURACY = 90

def run_model(prompt):

    response = client.responses.create(
    model="gpt-3.5-turbo",
    input=prompt
    )

    return response.output_text

def mock_run_model(prompt):
    return """
```python \n
import pytest
from source_files.maths_utils import add, subtract, multiply, divide, factorial, is_prime

# Test cases for add(a, b) function
def test_add_normal():
    assert add(2, 3) == 5

def test_add_edge():
    assert add(0, 5) == 5

def test_add_error():
    with pytest.raises(TypeError):
        add("2", 3)

# Test cases for subtract(a, b) function
def test_subtract_normal():
    assert subtract(5, 2) == 3

def test_subtract_edge():
    assert subtract(5, 0) == 5

def test_subtract_error():
    with pytest.raises(TypeError):
        subtract(5, "2")

# Test cases for multiply(a, b) function
def test_multiply_normal():
    assert multiply(3, 4) == 12

def test_multiply_edge():
    assert multiply(5, 0) == 0

def test_multiply_error():
    with pytest.raises(TypeError):
        multiply("3", 4)

# Test cases for divide(a, b) function
def test_divide_normal():
    assert divide(10, 2) == 5

def test_divide_edge():
    assert divide(10, 1) == 10

def test_divide_error():
    with pytest.raises(ValueError):
        divide(10, 0)

# Test cases for factorial(n) function
def test_factorial_normal():
    assert factorial(5) == 120

def test_factorial_edge():
    assert factorial(0) == 1

def test_factorial_error():
    with pytest.raises(ValueError):
        factorial(-5)

# Test cases for is_prime(n) function
def test_is_prime_normal():
    assert is_prime(7) == True

def test_is_prime_edge():
    assert is_prime(0) == False
    assert is_prime(1) == False

def test_is_prime_error():
    assert is_prime(-4) == False
```
"""

def clean_code_block(text):
    # Remove any leading code fence (with optional language)
    text = re.sub(r"^\s*```(?:\w+)?\s*", "", text)
    # Remove any trailing code fence
    text = re.sub(r"\s*```\s*$", "", text)
    return text.strip()

def run_pytest_with_coverage(path):
    cov = coverage.Coverage()
    cov.start()

    # Capture pytest output
    stdout = io.StringIO()
    stderr = io.StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = stdout, stderr

    try:
        exit_code = pytest.main([path])
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
        cov.stop()
        cov.save()

    out = stdout.getvalue()
    err = stderr.getvalue()

    # Get total coverage percentage
    total_coverage = cov.report(show_missing=False)

    return exit_code, out, err, total_coverage

def append_tests_to_file(test_code, test_filename="tests/test_math_utils.py"):
    # Clean code fences, then append
    def clean_code_block(text):
        if text.startswith("```"):
            first_newline = text.find("\n")
            text = text[first_newline+1:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    clean_code = clean_code_block(test_code)
    with open(test_filename, "a") as f:
        f.write("\n\n" + clean_code)

def get_failures_from_output(output_text):
    # Simple heuristic to extract failure summaries (can be improved)
    if "FAILED" in output_text:
        # Extract relevant lines or sections about failures
        # (You could parse pytest's summary or error trace)
        return output_text
    return None

def fix_failures_with_llm(failure_text):
    '''
    prompt = (
        "Analyze these pytest failure messages and suggest fixes or improved tests:\n"
        + failure_text
    )

    fix_code = run_model("small", prompt)
    append_tests_to_file(fix_code)
    '''
    print(failure_text)

def main():

    source_files = [file for file in os.listdir("source_files/") if file.endswith('.py')]
    print(source_files)
    for fp in source_files:
        print(fp)
        if not os.path.exists(f"tests/test_{fp}"):

            with open(f"source_files/{fp}", mode='r') as f:
                code = f.read()

            test_code = ""

            test_code += "import pytest \n"
            test_code += f"import source_files.{fp[:-3]} as testfile \n"

            testing_plan = run_model(
                                     prompt = "You are a senior testing engineer. Write a (text) PLAN for unit tests for this code covering normal, edge, and error cases:\n" + code + "file path: source_files/"+fp
                                     )

            test_code += run_model(
                                  prompt = "You are a senior testing engineer. Write GOOD QUALITY, high coverage PYTEST tests based on a testing plan. You should output string-wrapped python code which can directly be written to a python file. For every unit test, when you call a function, call it as 'testfile'.function e.g 'testfile.add()'. DO NOT TRY TO IMPORT ANY LIBRARIES -- this will be done manually. Return ONLY the code, nothing else -- your output will directly be written to a .py file with NO preprocessing. Output only the code with no markdown fences. Testing plan: \n" + testing_plan + "\nCode:\n" + code
                                  )

            test_filepath = f"tests/test_{fp}"
            with open(test_filepath, mode="w") as f:
                f.write(clean_code_block(test_code))

    current_coverage = 0
    previous_coverage = -1
    while current_coverage < TARGET_COVERAGE:
        exit_code, out, err, current_coverage = run_pytest_with_coverage(path="tests/")

        if exit_code != 0:
            failures = get_failures_from_output(out)
            fix_failures_with_llm(failures)

        print(f"Current coverage: {current_coverage:.2f}%")

    print("COVERAGE REACHED.... EXITING")


if __name__ == "__main__":
    main()



