# Lab 5: Static Code Analysis

## Objective
To improve Python code quality, security, and formatting using Pylint, Bandit, and Flake8.

## Issues Identified and Fixes

| Issue | Tool | Fix Applied |
|---|---|---|
| Hardcoded password | Bandit B105 | Read the password from an environment variable |
| Assert used for validation | Bandit B101 | Replaced assert with explicit validation |
| Insecure temporary-file creation | Bandit B306 | Used NamedTemporaryFile |
| Shell command execution | Bandit B605 | Removed unconfigured shell execution |
| Mutable default argument | Pylint | Changed notes=[] to notes=None |
| Broad exception handling | Pylint | Validated blood group before calculation |
| Missing documentation and naming issues | Pylint | Added docstrings and snake_case names |
| Formatting violations | Flake8 | Corrected spacing and blank lines |

## Final Results

- Pylint: 10.00/10
- Bandit: No issues identified
- Flake8: No violations reported

## Reflection

### 1. What is static code analysis?
Static code analysis examines source code without executing it to identify potential bugs, security issues, and style violations.

### 2. What is the difference between Pylint, Bandit, and Flake8?
Pylint checks code quality, Bandit checks common security problems, and Flake8 checks coding style and common errors.

### 3. Why is static analysis important?
It helps detect problems early, improve maintainability, and reduce security risks.

### 4. What challenges did you face?
Some warnings required understanding the underlying issue and modifying the code instead of simply suppressing the warning.

### 5. What did you learn?
I learned how to run static analysis tools, interpret their reports, fix code issues, and verify the changes using before-and-after reports.
