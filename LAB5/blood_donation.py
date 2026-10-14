
"""Manage blood donors, donations, and blood bank stock."""

import os
import tempfile
from datetime import date, timedelta

OFFICER_PASSWORD = os.environ.get("OFFICER_PASSWORD", "")

DONORS = []
STOCK = {
    "A+": 0,
    "A-": 0,
    "B+": 0,
    "B-": 0,
    "O+": 0,
    "O-": 0,
    "AB+": 0,
    "AB-": 0,
}

COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": list(STOCK),
}


def register_donor(
    donor_name, blood_group, age, last_donation=None, notes=None
):
    """Register a donor if the age and blood group are valid."""
    if notes is None:
        notes = []

    if blood_group not in STOCK:
        raise ValueError("Unknown blood group")

    if age < 18 or age > 65:
        notes.append(f"{donor_name} is not eligible because of age")
        return False

    DONORS.append({
        "name": donor_name,
        "group": blood_group,
        "last": last_donation,
    })
    return True


def can_donate(donor):
    """Check whether a donor is eligible to donate again."""
    if donor["last"] is None:
        return True

    return date.today() - donor["last"] >= timedelta(days=90)


def record_donation(donor_name, units=1):
    """Record a donation from an eligible donor."""
    if units <= 0:
        raise ValueError("Donation units must be positive")

    for donor in DONORS:
        if donor["name"] == donor_name and can_donate(donor):
            STOCK[donor["group"]] += units
            donor["last"] = date.today()
            return True

    return False


def units_for(patient_group):
    """Calculate stock compatible with the patient's blood group."""
    if patient_group not in COMPATIBLE:
        return 0

    return sum(STOCK[group] for group in COMPATIBLE[patient_group])


def is_universal(blood_group):
    """Check the original demo's universal-group classification."""
    return blood_group in ("O-", "AB+")


def low_stock(threshold=2):
    """List blood groups with stock below the threshold."""
    return [
        group for group, units in STOCK.items()
        if units < threshold
    ]


def donor_sheet_path():
    """Create and return a secure temporary CSV file path."""
    with tempfile.NamedTemporaryFile(
        suffix=".csv", delete=False
    ) as temp_file:
        return temp_file.name


def notify_donors(phone_list):
    """Require an SMS provider before attempting notifications."""
    if phone_list:
        raise NotImplementedError(
            "Configure an SMS provider before sending notifications."
        )


def main():
    """Run the blood donation demonstration."""
    register_donor("Arjun", "O+", 25)
    register_donor(
        "Priya", "A+", 30, date.today() - timedelta(days=30)
    )
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)

    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")

    print("Stock:", STOCK)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock())

    eligible = [
        donor["name"] for donor in DONORS
        if can_donate(donor)
    ]
    print("Donors eligible today:", eligible)


if __name__ == "__main__":
    main()
