# L6_L7_28 — Airline Baggage Fees

Lab 6: Code and Branch Coverage

## About

A small Python module that works out baggage fees by cabin, route and membership, checks carry-on limits and reports check-in counter status.

## Files

| File | Description |
|------|-------------|
| `airline_baggage.py` | The module under test |
| `test_airline_baggage.py` | Starter test file |
| `CodeCoverageTest_28_airline_baggage.py` | Tests for line/code coverage |
| `BranchCoverageTest_28_airline_baggage.py` | Tests for decision branch coverage |

## Run the coverage suites

Run these commands from this directory after installing `pytest` and `coverage`:

```powershell
python -m coverage erase
python -m coverage run --source=airline_baggage -m pytest CodeCoverageTest_28_airline_baggage.py
python -m coverage report -m
```

The code-coverage suite passes 22 tests and reports 100% line coverage. Its
terminal output is saved in `code_coverage_results.png` and
`code_coverage_results.txt`.

For branch coverage, start with a clean measurement:

```powershell
python -m coverage erase
python -m coverage run --branch --source=airline_baggage -m pytest BranchCoverageTest_28_airline_baggage.py
python -m coverage report -m
```

The branch-coverage suite passes 21 tests and reports 100% branch coverage
(26/26 branches). Its terminal output is saved in `branch_coverage_results.png`
and `branch_coverage_results.txt`.
