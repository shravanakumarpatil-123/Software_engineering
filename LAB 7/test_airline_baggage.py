"""Property-based and regression tests for the baggage input functions."""

import math
import string

import pytest
from hypothesis import given, settings, strategies as st

from airline_baggage import parse_booking, tag_label, total_weight


# Use a fixed seed so the failing examples included in the lab report are
# repeatable. Hypothesis still shrinks each failure to a small counterexample.
FUZZ_SETTINGS = settings(max_examples=100, deadline=None, derandomize=True)

UNEXPECTED_INPUTS = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.lists(st.text()),
)


@FUZZ_SETTINGS
@given(value=UNEXPECTED_INPUTS)
def test_parse_booking_handles_unexpected_inputs(value):
    """The parser returns None for invalid input instead of leaking errors."""
    result = parse_booking(value)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 3
        and isinstance(result[0], str)
        and result[0].isalpha()
        and result[0] == result[0].upper()
        and isinstance(result[1], int)
        and result[1] > 0
        and isinstance(result[2], str)
        and len(result[2]) == 1
        and result[2].isalpha()
        and result[2] == result[2].upper()
    )


@FUZZ_SETTINGS
@given(
    airline=st.text(alphabet=string.ascii_letters, min_size=2, max_size=3),
    flight=st.integers(min_value=1, max_value=9999),
    row=st.integers(min_value=1, max_value=99),
    seat=st.sampled_from(string.ascii_letters),
)
def test_parse_booking_preserves_valid_booking_codes(airline, flight, row, seat):
    code = f"{airline}-{flight}-{row}{seat}"
    assert parse_booking(code) == (airline.upper(), flight, seat.upper())


@pytest.mark.parametrize(
    "value",
    [None, "", "AI-203", "AI-x-12A", "AI-203-12", "A-203-12A", "AI-0-12A"],
)
def test_parse_booking_rejects_malformed_codes(value):
    assert parse_booking(value) is None


@FUZZ_SETTINGS
@given(value=UNEXPECTED_INPUTS)
def test_total_weight_handles_unexpected_inputs(value):
    """The weight parser returns None for invalid input and finite totals."""
    result = total_weight(value)
    assert result is None or (
        isinstance(result, float) and math.isfinite(result) and result >= 0
    )


@FUZZ_SETTINGS
@given(
    weights=st.lists(
        st.floats(min_value=0, max_value=100_000, allow_nan=False, allow_infinity=False),
        min_size=1,
    )
)
def test_total_weight_sums_valid_csv_values(weights):
    csv = ",".join(repr(weight) for weight in weights)
    assert total_weight(csv) == pytest.approx(math.fsum(weights))


@pytest.mark.parametrize("value", [None, "", "1,,2", "1,heavy", "-1,2", "nan", "inf"])
def test_total_weight_rejects_malformed_or_unsafe_values(value):
    assert total_weight(value) is None


@FUZZ_SETTINGS
@given(value=UNEXPECTED_INPUTS)
def test_tag_label_handles_unexpected_inputs(value):
    """The name formatter returns None when it cannot build a useful label."""
    result = tag_label(value)
    assert result is None or (
        isinstance(result, str)
        and len(result) >= 4
        and result[0].isalpha()
        and result[0] == result[0].upper()
        and result[1:3] == ". "
        and result[3:].isalpha()
        and result[3:] == result[3:].upper()
    )


@FUZZ_SETTINGS
@given(
    first=st.text(alphabet=string.ascii_letters, min_size=1, max_size=15),
    middle=st.text(alphabet=string.ascii_letters, min_size=1, max_size=15),
    last=st.text(alphabet=string.ascii_letters, min_size=1, max_size=15),
)
def test_tag_label_uses_first_initial_and_last_name(first, middle, last):
    assert tag_label(f"{first} {middle} {last}") == f"{first[0].upper()}. {last.upper()}"


@pytest.mark.parametrize("value", [None, "", "   ", "OnlyFirstName"])
def test_tag_label_rejects_incomplete_names(value):
    assert tag_label(value) is None


def test_lab_examples():
    assert parse_booking("AI-203-12A") == ("AI", 203, "A")
    assert total_weight("12.5, 7,23") == pytest.approx(42.5)
    assert tag_label("John Doe") == "J. DOE"
