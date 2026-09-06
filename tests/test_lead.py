import pytest
from backend.models import Lead


# Test updating a lead status
def test_update_status():

    lead = Lead(1, 1111, "Cumberland", "Spray", "Created")

    lead.update_status("Sent")

    assert lead.status == "Sent"


# Test updating a lead with an invalid status
def test_invalid_lead_status():

    lead = Lead(1, 1111, "Cumberland", "Spray", "Created")

    with pytest.raises(ValueError):
        lead.update_status("Banana")


# Test an invalid lead status transition
def test_invalid_lead_status_transition():

    lead = Lead(1, 1111, "Cumberland", "Spray", "Created")

    with pytest.raises(ValueError):
        lead.update_status("Won")


# Test the complete lead workflow
def test_complete_lead_workflow():

    lead = Lead(1, 1111, "Cumberland", "Spray", "Created")

    lead.update_status("Sent")
    lead.update_status("Received")
    lead.update_status("Survey")
    lead.update_status("Quote")
    lead.update_status("Won")

    assert lead.status == "Won"


# Test losing a lead after a quote
def test_quote_to_lost():

    lead = Lead(1, 1111, "Cumberland", "Spray", "Quote")

    lead.update_status("Lost")

    assert lead.status == "Lost"