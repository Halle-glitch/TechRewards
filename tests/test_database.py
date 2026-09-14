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


database.set_database(":memory:")


@pytest.fixture(autouse=True)
def clean_database():

    # Clear the database before each test
    cursor = database.connection.cursor()

    cursor.execute("DELETE FROM leads")
    cursor.execute("DELETE FROM rewards")

    database.connection.commit()

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


# Test getting all leads for a technician
def test_get_leads_by_technician():

    create_lead(
        106,
        "Customer One",
        "Spray",
        "Created"
    )

    create_lead(
        106,
        "Customer Two",
        "Rodent proofing",
        "Sent"
    )

    create_lead(
        107,
        "Other Customer",
        "Cockroach treatment",
        "Created"
    )

    leads = get_leads_by_technician(106)

    assert len(leads) == 2
    assert leads[0][1] == 106
    assert leads[0][2] == "Customer One"
    assert leads[1][1] == 106
    assert leads[1][2] == "Customer Two"


# Test getting leads for a technician with no leads
def test_get_leads_for_technician_with_no_leads():

    leads = get_leads_by_technician(9999)

    assert leads == []


# Test creating a new reward
def test_create_reward():

    reward_id = create_reward(
        101,
        "Trustpilot",
        10,
        "5-star customer reveiw"
    )

    assert reward_id is not None


# Test that negative rewards are rejected
def test_create_reward_negative_amount():

    with pytest.raises(ValueError):
        create_reward(
            101,
            "Trustpilot",
            -10,
            "5-star customer review"
        )


# Test getting rewards for a technician
def test_get_rewards_by_technician():

    create_reward(
        101,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    create_reward(
        101,
        "CVC",
        50,
        "Technician named in 10/10 feedback"
    )

    create_reward(
        102,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    rewards = get_rewards_by_technician(101)

    assert len(rewards) == 2
    assert rewards[0][1] == 101
    assert rewards[0][2] == "Trustpilot"
    assert rewards[0][3] == 10

    assert rewards[1][1] == 101
    assert rewards[1][2] == "CVC"
    assert rewards[1][3] == 50


# Test getting rewards for a technician with no rewards
def test_get_rewards_for_technician_with_no_rewards():

    rewards = get_rewards_by_technician(9999)

    assert rewards == []


# Test getting a reward
def test_get_reward():

    reward_id = create_reward(
        101,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    reward = get_reward(reward_id)

    assert reward[0] == reward_id
    assert reward[1] == 101
    assert reward[2] == "Trustpilot"
    assert reward[3] == 10
    assert reward[4] == "5-star customer review"


# Test getting the total rewards for a technician
def test_get_total_rewards_by_technician():

    create_reward(
        101,
        "Trustpilot",
        10,
        "5-star customer review"
    )

    create_reward(
            101,
            "CVC",
            50,
            "Technician named in 10/10 feedback"
        )

    create_reward(
            101,
            "Referral",
            1000,
            "Referral completed 6 months"
        )

    total = get_total_rewards_by_technician(101)

    assert total == 1060


# Test getting total rewards when there are no rewards
def test_get_total_rewards_with_no_rewards():

    total = get_total_rewards_by_technician(9999)

    assert total == 0

def test_create_lead_commission_reward():
    reward_id = create_lead_commission_reward(
        101,
        7000,
        1000,
        "Lead converted"
    )

    reward = get_reward(reward_id)

    assert reward[1] == 101
    assert reward[2] == "Lead Commission"
    assert reward[3] == 50
    assert reward[4] == "Lead converted"


def test_create_lead_commission_reward_crossing_threshold():
    reward_id = create_lead_commission_reward(
        101,
        2400,
        500,
        "Lead crossing threshold"
    )

    reward = get_reward(reward_id)

    assert reward[3] == 18.5


def test_get_total_lead_commission_by_technician():
    create_reward(
        101,
        "Lead Commission",
        50,
        "First lead"
    )

    create_reward(
        101,
        "Lead Commission",
        18.5,
        "Second lead"
    )

    create_reward(
        101,
        "Trustpilot",
        10,
        "Five-star review"
    )

    total = get_total_lead_commission_by_technician(101)

    assert total == 68.5


def test_no_lead_commission_returns_zero():
    total = get_total_lead_commission_by_technician(101)

    assert total == 0



def test_create_technician():
    technician_id = create_technician(
        "Miguel",
        "RT001"
    )

    technician = get_technician(technician_id)

    assert technician[0] == technician_id
    assert technician[1] == "Miguel"
    assert technician[2] == "RT001"


def test_get_missing_technician():
    technician = get_technician(999)

    assert technician is None