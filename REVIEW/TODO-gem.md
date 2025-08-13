# TODO and Improvement Proposals for `fontlab_export_tools`

This document outlines a plan and specific ideas for improving the `fontlab_export_tools` repository. The proposals focus on enhancing the documentation, testing, and code quality.

## 1. Enhance the `README.md`

The current `README.md` is a template from PyScaffold. It should be updated to provide a clear and concise overview of the project.

**Proposal:**

-   **Add a detailed project description:** Explain what `fontlab_export_tools` does, who it is for, and what problems it solves.
-   **Include a "Features" section:** List the key features of the library and CLI tools.
-   **Provide installation instructions:** Explain how to install the package, possibly with `pip`.
-   **Add a "Usage" section:** Provide clear examples of how to use the CLI tools and the Python library.

**Example of an improved `README.md` section:**

```markdown
## Usage

### Command-Line Interface

To export a FontLab file to UFO format, you can use the `fl-export` command:

```bash
fl-export --input /path/to/font.vfc --output /path/to/font.ufo
```

### Python Library

You can also use the library directly in your Python scripts:

```python
from fontlab_export_tools import export_to_ufo

export_to_ufo("/path/to/font.vfc", "/path/to/font.ufo")
```

## 2. Improve the Documentation

The documentation in the `docs/` directory is also a template. It should be expanded to provide comprehensive information about the project.

**Proposal:**

-   **Create a "Getting Started" guide:** A tutorial that walks new users through the process of installing and using the tools.
-   **Add an API reference:** Detailed documentation for all public modules, classes, and functions in the `fontlab_export_tools` package. This can be generated from docstrings using a tool like Sphinx's `autodoc`.
-   **Document the CLI tools:** A dedicated page explaining how to use each CLI tool, including all available options and arguments.
-   **Explain the FontLab integration:** Provide details on how the `.vfpy` scripts work and how to use them within FontLab.

## 3. Expand the Test Suite

The current test suite in `tests/test_skeleton.py` is a placeholder. A robust test suite is crucial for ensuring the reliability of the tools.

**Proposal:**

-   **Add unit tests:** Write unit tests for all functions in the `src/fontlab_export_tools/` directory. For example, test the utility functions in `utils.py` and the Git functions in `git.py`.
-   **Add integration tests:** Create tests that verify the end-to-end functionality of the CLI tools. This could involve running the tools on sample FontLab files and checking the output.
-   **Use a mocking framework:** Use a library like `pytest-mock` to mock external dependencies, such as the FontLab application itself, to allow for testing without a full FontLab installation.
-   **Aim for high test coverage:** Use `coverage.py` to measure test coverage and strive for a high percentage of covered code.

**Example of a new test file `tests/test_utils.py`:**

```python
from fontlab_export_tools import utils

def test_some_utility_function():
    # Test case for a utility function
    assert utils.some_utility_function(1, 2) == 3
```

## 4. Refactor the Code

The code is generally well-structured, but there are a few areas that could be improved.

**Proposal:**

-   **Add type hints:** Add type hints to all function signatures to improve code clarity and allow for static analysis.
-   **Use a consistent coding style:** Ensure that the entire codebase follows the PEP 8 style guide. Tools like `black` and `flake8` can automate this.
-   **Refactor `make.py`:** If the `make.py` script becomes complex, consider refactoring it into smaller, more manageable functions or classes.

**Example of a function with type hints:**

```python
def export_to_ufo(input_path: str, output_path: str) -> None:
    """
    Exports a FontLab file to UFO format.
    """
    # Implementation here
    ...
```
