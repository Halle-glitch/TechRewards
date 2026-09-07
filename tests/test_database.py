import pytest
from backend.database import create_lead, get_lead, update_lead_status


# Test creating a new lead
def test_create_lead():

    lead_id = create_lead(
        101,
        "Cumberland",
        "Spray",
        "Created"
    )

    assert lead_id is not None


# TEST getting a lead
def test_get_lead():

    lead_id = create_lead(
        102,
        "Test Customer",
        "Rodent proofing",
        "Created",
    )

    lead = get_lead(lead_id)

    assert lead[0] == lead_id
    assert lead[1] == 102
    assert lead[2] == "Test Customer"
    assert lead[3] == "Rodent proofing"
    assert lead[4] == "Created"


# Test updating a lead status
def test_update_lead_status():

    lead_id = create_lead(
        103,
        "Update Customer",
        "Cockroach treatment",
        "Created"
    )

    update_lead_status(lead_id, "Sent")

    lead = get_lead(lead_id)

    assert lead[4] == "Sent"


#Test an invalid lead status transition
def test_invalid_lead_status_transition():

    lead_id = create_lead(
        104,
        "Invalid Customer",
        "Spray",
        "Created"
    )

    with pytest.raises(ValueError):
        update_lead_status(lead_id, "Won")


# Test creating a lead with an invalid status
def test_invalid_lead_status():

    with pytest.raises(ValueError):
        create_lead(
            105,
            "Invalid Customer",
            "Spray",
            "Banana"
        )