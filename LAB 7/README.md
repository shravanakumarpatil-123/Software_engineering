# LAB 7: Fuzz Testing

This folder adapts the supplied airline baggage lab to the attached Lab 7 handout. The source repository uses `airline_baggage.py` and `test_airline_baggage.py` instead of the generic `processor.py` names shown in the handout.

## What the lab covers

- Fuzzes `parse_booking`, `total_weight`, and `tag_label` with Hypothesis, including strings, `None`, numbers, and lists.
- Captures the original failures, hardens the three functions, and reruns the same suite.
- Includes the four command output captures in `screenshots/` and a printable summary in `Lab_7_FuzzTesting_Report.pdf`.

Invalid inputs return `None`. Valid inputs keep the expected result shape. Booking codes must use a 2-3 letter airline code, a positive numeric flight number, and a numeric seat row followed by one letter. Weight entries must be finite, nonnegative numbers. Passenger labels use the first initial and final name.

## Run the lab

From this folder, install the dependencies and run the application and property-based tests:

```powershell
python -m pip install -r requirements.txt
python airline_baggage.py
python -m pytest -q test_airline_baggage.py
```

Example inputs for the application are `AI-203-12A`, `12.5,7,23`, and `John Doe`.

The test suite includes repeatable Hypothesis tests for unexpected values and generated valid values, plus regression cases for malformed bookings, weights, and names.
