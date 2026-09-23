import sqlite3
from backend.rules import LEAD_STATUSES, LEAD_STATUS_TRANSITIONS

# connect to database
def connect_to_database(database_path="techrewards.db"):

    # Allow the connection to work with FastAPI threads
    return sqlite3.connect(
        database_path,
        check_same_thread=False
    )

# Create the database connection
connection = connect_to_database()


# Change the database connection
def set_database(database_path):

    global connection

    # Close the current connection
    connection.close()

    # Create a new connection
    connection = connect_to_database(database_path)

    # Create the tables in the new database
    create_tables()


# Create the database tables
def create_tables():

    # Create a cursor
    cursor = connection.cursor()

    # Create the technicians table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS technicians (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            employee_number TEXT NOT NULL
        )
    """)

    # Create the leads table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY,
            technician_id INTEGER NOT NULL,
            customer TEXT NOT NULL,
            opportunity TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Create the rewards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rewards (
            id INTEGER PRIMARY KEY,
            technician_id INTEGER NOT NULL,
            reward_type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL
        )
    """)

    # Save the changes
    connection.commit()

# Create the tables
create_tables()




# Create a new lead
def create_lead(technician_id, customer, opportunity, status):

    # Check if the status is valid
    if status not in LEAD_STATUSES:
        raise ValueError("Invalid lead status")

    # Create a cursor
    cursor = connection.cursor()

    # Add the lead to the database
    cursor.execute("""
        INSERT INTO leads (
            technician_id,
            customer,
            opportunity,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        technician_id,
        customer,
        opportunity,
        status
    ))

    # Save the changes
    connection.commit()

    # Return the ID of the new lead
    return cursor.lastrowid


# Get a lead from the database
def get_lead(lead_id):

    # Create a cursor
    cursor = connection.cursor()

    # Find the lead with this ID
    cursor.execute("""
        SELECT id, technician_id, customer, opportunity, status
        FROM leads
        WHERE id = ?
    """, (lead_id,))

    # Get the resutl
    lead = cursor.fetchone()

    # Return the lead
    return lead


# Get all leads for a technician
def get_leads_by_technician(technician_id):

    # Create a cursor
    cursor = connection.cursor()

    # Find all leads for this technician
    cursor.execute("""
        SELECT id, technician_id, customer, opportunity, status
        FROM leads
        WHERE technician_id = ?
    """, (technician_id,))

    # Get all matching leads
    leads = cursor.fetchall()

    # Return the leads
    return leads


# Update the status of a lead
def update_lead_status(lead_id, new_status):

    #Get the current lead
    lead = get_lead(lead_id)

    # Check if the lead exists
    if lead is None:
        raise ValueError("Lead not found")

    # Get the current status
    current_status = lead[4]

    # Get the allowed next statuses
    allowed_statuses = LEAD_STATUS_TRANSITIONS[current_status]

    # Check if the new status is allowed
    if new_status not in allowed_statuses:
        raise ValueError("Invalid lead status transtion")

    # Create a cursor
    cursor = connection.cursor()

    # Update the lead status
    cursor.execute("""
        UPDATE leads
        SET status = ?
        WHERE id = ?
        """, (
            new_status,
            lead_id
            ))

    # SAve the changes
    connection.commit()


# Create a new reward
def create_reward(technician_id, reward_type, amount, description):

    # Check that the reward amount is valid
    if amount < 0:
        raise ValueError("Reward amount cannot be negative")

    # Create a cursor
    cursor = connection.cursor()

    # Add the reward to the database
    cursor.execute("""
        INSERT INTO rewards (
            technician_id,
            reward_type,
            amount,
            description
        )
        VALUES (?, ?, ?, ?)
    """, (
        technician_id,
        reward_type,
        amount,
        description
    ))

    # Save the changes
    connection.commit()

    # Return the ID of the new reward
    return cursor.lastrowid


# Get all rewards for a technician
def get_rewards_by_technician(technician_id):

    # Create a cursor
    cursor = connection.cursor()

    # Find all rewards for the technician
    cursor.execute("""
        SELECT id, technician_id, reward_type, amount, description
        FROM rewards
        WHERE technician_id = ?
    """, (technician_id,))

    # Get all matching rewards
    rewards = cursor.fetchall()

    # Return the rewards
    return rewards


# Get a reward from the database
def get_reward(reward_id):

    # Crete a cursor
    cursor = connection.cursor()

    # Find the reward with this ID
    cursor.execute("""
    SELECT id, technician_id, reward_type, amount, description
    FROM rewards
    WHERE id = ?
    """, (reward_id,))

    # Get the result
    reward = cursor.fetchone()

    # Return the reward
    return reward


# Get the total rewards for  a technician
def get_total_rewards_by_technician(technician_id):

    # Create a cursor
    cursor = connection.cursor()

    # Add all reward amounts together
    cursor.execute("""
    SELECT SUM(amount)
    FROM rewards
    WHERE technician_id = ?
    """, (technician_id,))

    # Get the result
    total = cursor.fetchone()[0]

    # Return zero if there are no rewards
    if total is None:
        return 0

    # Return the total rewards
    return total


# Create a lead commission reward
def create_lead_commission_reward(
    technician_id,
    total_converted,
    sale_value,
    description
):

    # Import the commission calculation
    from backend.commission import calculate_lead_commission

    # Calculate the commission
    commission = calculate_lead_commission(
        total_converted,
        sale_value
    )

    # Save the commission as a reward
    reward_id = create_reward(
        technician_id,
        "Lead Commission",
        commission,
        description
    )

    # Return the reward ID
    return reward_id


# Get total lead commission for a technician
def get_total_lead_commission_by_technician(technician_id):

    # Create a cursor
    cursor = connection.cursor()

    # Find all lead commission rewards for this technician
    cursor.execute(
        """
        SELECT SUM(amount)
        FROM rewards
        WHERE technician_id = ?
        AND reward_type = ?
        """,
        (technician_id, "Lead Commission")
    )

    # Get the result
    result = cursor.fetchone()[0]

    # Return zero if there are no lead commissions
    if result is None:
        return 0

    # Return the total commission
    return result


# Create a new technician
def create_technician(name, employee_number):

    # Create a cursor
    cursor = connection.cursor()

    # Add the technician to the database
    cursor.execute("""
        INSERT INTO technicians (
            name,
            employee_number
        )
        VALUES (?, ?)
    """, (
        name,
        employee_number
    ))

    # Save the changes
    connection.commit()

    # Return the ID of the new technician
    return cursor.lastrowid

# Get a technician from the database
def get_technician(technician_id):

    # Create a cursor
    cursor = connection.cursor()

    # Find the technician with this ID
    cursor.execute("""
        SELECT id, name, employee_number
        FROM technicians
        WHERE id = ?
    """, (technician_id,))

    # Get the result
    technician = cursor.fetchone()

    # Return the technician
    return technician


def get_lead_counts_by_technician(technician_id):
    # Get lead counts for one technician
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
        COUNT(*),
        SUM(CASE WHEN status = 'Won' THEN 1 ELSE 0 END),
        SUM(CASE WHEN status = 'Lost' THEN 1 ELSE 0 END)
        FROM leads
        WHERE technician_id = ?
        """, (technician_id,)
    )

    result = cursor.fetchone()

    return {
        "total_leads": result[0],
        "won_leads": result[1] or 0,
        "lost_leads": result[2] or 0,
    }