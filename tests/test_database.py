import pytest
import backend.database as database

from backend.database import (
    create_lead,
    get_lead,
    get_leads_by_technician,
    update_lead_status,
    create_reward,
    get_rewards_by_technician,
    get_reward,
    get_total_rewards_by_technician,
    create_lead_commission_reward,
    get_total_lead_commission_by_technician,
    create_technician,
    get_technician,
)


# Use a temporary database for the tests
database.set_database(":memory:")


# Run this before every test
@pytest.fixture(autouse=True)
def clean_database():

    # Open the database
    cursor = database.connection.cursor()

    # Delete all leads from the previous test
    cursor.execute("DELETE FROM leads")

    # Delete all rewards from the previous test
    cursor.execute("DELETE FROM rewards")

    # Delete all technicians from the previous test
    cursor.execute("DELETE FROM technicians")

    # Save the changes
    database.connection.commit()


# Test creating a new lead
def test_create_lead():

    # Create a lead and save its ID
    lead_id = create_lead(
        101,
        "Cumberland",
        "Spray",
        "Created"
    )

    # Check that an ID was created
    assert lead_id is not None


# Test getting a lead
def test_get_lead():

    # Create a lead first
    lead_id = create_lead(
        102,
        "Test Customer",
        "Rodent proofing",
        "Created",
    )

    # Get the lead from the database
    lead = get_lead(lead_id)

    # Check that the returned information is correct
    assert lead[0] == lead_id
    assert lead[1] == 102
    assert lead[2] == "Test Customer"
    assert lead[3] == "Rodent proofing"
    assert lead[4] == "Created"


# Test updating a lead status
def test_update_lead_status():

    # Create a lead with the starting status
    lead_id = create_lead(
        103,
        "Update Customer",
        "Cockroach treatment",
        "Created"
    )

    # Change the lead status from Created to Sent
    update_lead_status(lead_id, "Sent")

    # Get the updated lead
    lead = get_lead(lead_id)

    # Check that the status changed correctly
    assert lead[4] == "Sent"


# Test an invalid lead status transition
def test_invalid_lead_status_transition():

    # Create a lead
    lead_id = create_lead(
        104,
        "Invalid Customer",
        "Spray",
        "Created"
    )

    # Check that an invalid change raises an error
    with pytest.raises(ValueError):
        update_lead_status(lead_id, "Won")


# Test creating a lead with an invalid status
def test_invalid_lead_status():

    # Try to create a lead with a status that does not exist
    with pytest.raises(ValueError):
        create_lead(
            105,
            "Invalid Customer",
            "Spray",
            "Banana"
        )


# Test getting all leads for a technician
def test_get_leads_by_technician():

    # Create the first lead for technician 106
    create_lead(
        106,
        "Customer One",
        "Spray",
        "Created"
    )

    # Create the second lead for technician 106
    create_lead(
        106,
        "Customer Two",
        "Rodent proofing",
        "Sent"
    )

    # Create a lead for another technician
    create_lead(
        107,
        "Other Customer",
        "Cockroach treatment",
        "Created"
    )

    # Get only the leads belonging to technician 106
    leads = get_leads_by_technician(106)

    # Check that only two leads were returned
    assert len(leads) == 2

    # Check the first lead
    assert leads[0][1] == 106
    assert leads[0][2] == "Customer One"

    # Check the second lead
    assert leads[1][1] == 106
    assert leads[1][2] == "Customer Two"


# Test getting leads for a technician with no leads
def test_get_leads_for_technician_with_no_leads():

    # Ask for leads belonging to a technician that does not exist
    leads = get_leads_by_technician(9999)

    # The result should be an empty list
    assert leads == []


# Test creating a new reward
def test_create_reward():

    # Create a Trustpilot reward
    reward_id = create_reward(
        101,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    # Check that an ID was created
    assert reward_id is not None


# Test that negative rewards are rejected
def test_create_reward_negative_amount():

    # Try to create a reward with a negative amount
    with pytest.raises(ValueError):
        create_reward(
            101,
            "Trustpilot",
            -10,
            "5-star customer review"
        )


# Test getting rewards for a technician
def test_get_rewards_by_technician():

    # Create a Trustpilot reward for technician 101
    create_reward(
        101,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    # Create a CVC reward for technician 101
    create_reward(
        101,
        "CVC",
        50,
        "Technician named in 10/10 feedback"
    )

    # Create a reward for another technician
    create_reward(
        102,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    # Get rewards for technician 101
    rewards = get_rewards_by_technician(101)

    # Check that only two rewards were returned
    assert len(rewards) == 2

    # Check the first reward
    assert rewards[0][1] == 101
    assert rewards[0][2] == "Trustpilot"
    assert rewards[0][3] == 10

    # Check the second reward
    assert rewards[1][1] == 101
    assert rewards[1][2] == "CVC"
    assert rewards[1][3] == 50


# Test getting rewards for a technician with no rewards
def test_get_rewards_for_technician_with_no_rewards():

    # Ask for rewards belonging to a technician that does not exist
    rewards = get_rewards_by_technician(9999)

    # The result should be an empty list
    assert rewards == []


# Test getting a reward
def test_get_reward():

    # Create a reward
    reward_id = create_reward(
        101,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    # Get the reward from the database
    reward = get_reward(reward_id)

    # Check that the reward information is correct
    assert reward[0] == reward_id
    assert reward[1] == 101
    assert reward[2] == "Trustpilot"
    assert reward[3] == 10
    assert reward[4] == "5-star customer review"


# Test getting the total rewards for a technician
def test_get_total_rewards_by_technician():

    # Create a Trustpilot reward
    create_reward(
        101,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    # Create a CVC reward
    create_reward(
        101,
        "CVC",
        50,
        "Technician named in 10/10 feedback"
    )

    # Create a referral reward
    create_reward(
        101,
        "Referral",
        1000,
        "Referral completed 6 months"
    )

    # Get the total value of all rewards
    total = get_total_rewards_by_technician(101)

    # Check that the total is correct
    assert total == 1060


# Test getting total rewards when there are no rewards
def test_get_total_rewards_with_no_rewards():

    # Get the total for a technician with no rewards
    total = get_total_rewards_by_technician(9999)

    # The total should be zero
    assert total == 0


# Test creating a lead commission reward
def test_create_lead_commission_reward():

    # Create a lead commission reward
    reward_id = create_lead_commission_reward(
        101,
        7000,
        1000,
        "Lead converted"
    )

    # Get the saved reward
    reward = get_reward(reward_id)

    # Check that the reward was saved correctly
    assert reward[1] == 101
    assert reward[2] == "Lead Commission"
    assert reward[3] == 50
    assert reward[4] == "Lead converted"


# Test lead commission when crossing a commission threshold
def test_create_lead_commission_reward_crossing_threshold():

    # Create a lead commission reward
    reward_id = create_lead_commission_reward(
        101,
        2400,
        500,
        "Lead crossing threshold"
    )

    # Get the saved reward
    reward = get_reward(reward_id)

    # Check that the commission was calculated correctly
    assert reward[3] == 18.5


# Test getting the total lead commission for a technician
def test_get_total_lead_commission_by_technician():

    # Create the first lead commission
    create_reward(
        101,
        "Lead Commission",
        50,
        "First lead"
    )

    # Create the second lead commission
    create_reward(
        101,
        "Lead Commission",
        18.5,
        "Second lead"
    )

    # Create a different type of reward
    create_reward(
        101,
        "Trustpilot",
        10,
        "Five-star review"
    )

    # Get only the total lead commission
    total = get_total_lead_commission_by_technician(101)

    # Check that the Trustpilot reward was not included
    assert total == 68.5


# Test getting lead commission when there are no lead commissions
def test_no_lead_commission_returns_zero():

    # Get the total for a technician with no lead commissions
    total = get_total_lead_commission_by_technician(101)

    # The total should be zero
    assert total == 0


# Test creating a technician
def test_create_technician():

    # Create a technician and get the new ID
    technician_id = create_technician(
        "Miguel",
        "RT001"
    )

    # Get the technician from the database
    technician = get_technician(technician_id)

    # Check that the technician information is correct
    assert technician[0] == technician_id
    assert technician[1] == "Miguel"
    assert technician[2] == "RT001"


# Test getting a technician that does not exist
def test_get_missing_technician():

    # Try to get a technician with an ID that does not exist
    technician = get_technician(999)

    # The result should be None
    assert technician is None