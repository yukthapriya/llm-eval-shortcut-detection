"""
grader/__init__.py
Runs each task against Llama 3.3 70B via Groq, scores surface and invariant tests,
and returns structured results.
"""

import subprocess
import sys
import tempfile
import os
import time
from dataclasses import dataclass
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"


@dataclass
class TaskResult:
    id: str
    title: str
    failure_category: str
    description: str
    surface_pass: bool
    invariant_pass: bool
    surface_error: str
    invariant_error: str
    model_code: str


def ask_model(prompt: str) -> str:
    """Send task prompt to Groq and return the raw response."""
    full_prompt = f"""{prompt}

Return only the Python function. No explanation. No test code.

Format:
```python
def solution(...):
    ...
```"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content


def extract_code(text: str) -> str:
    """Extract Python code block from model response."""
    if "```python" in text:
        start = text.index("```python") + 9
        end = text.index("```", start)
        return text[start:end].strip()
    if "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        return text[start:end].strip()
    return text.strip()


def run_tests(code: str, tests: str) -> tuple[bool, str]:
    """
    Execute code + tests in a subprocess.
    Returns (passed, error_snippet).
    """
    full = code + "\n\n" + tests
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(full)
        fname = f.name
    try:
        result = subprocess.run(
            [sys.executable, fname],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0:
            return True, ""
        err = (result.stderr or result.stdout).strip()
        return False, err[-400:]
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: execution exceeded 20 seconds"
    except Exception as e:
        return False, str(e)
    finally:
        try:
            os.unlink(fname)
        except Exception:
            pass


def grade_task(task) -> TaskResult:
    """Grade a single task against the model."""
    raw = ask_model(task.prompt)
    time.sleep(2)  # stay within Groq free tier rate limits
    code = extract_code(raw)

    surface_pass, surface_err = run_tests(code, task.surface_tests)
    invariant_pass, invariant_err = run_tests(code, task.invariant_tests)

    return TaskResult(
        id=task.id,
        title=task.title,
        failure_category=task.failure_category,
        description=task.description,
        surface_pass=surface_pass,
        invariant_pass=invariant_pass,
        surface_error=surface_err,
        invariant_error=invariant_err,
        model_code=code,
    )


def grade_all(tasks, progress_callback=None) -> list[TaskResult]:
    """Grade all tasks. Calls progress_callback(i, total, result) after each."""
    results = []
    for i, task in enumerate(tasks):
        result = grade_task(task)
        results.append(result)
        if progress_callback:
            progress_callback(i + 1, len(tasks), result)
    return results