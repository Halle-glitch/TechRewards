from backend.rules import LEAD_STATUSES, LEAD_STATUS_TRANSITIONS

#Tech model
#Storing basic info about a technician

class Technician:

    # create a new technician
    def __init__(self, id, name, employee_number):

        # saveing the tech info
        self.id = id
        self.name = name
        self.employee_number = employee_number


class Lead:

    def __init__(self, id, technician_id, customer, opportunity, status):

        self.id = id
        self.technician_id = technician_id
        self.customer = customer
        self.opportunity = opportunity

        # Check if the status is valid
        if status not in LEAD_STATUSES:
            raise ValueError("Invalid lead status")

        self.status = status

    def update_status(self, new_status):

        # Check if the new status is valid
        if new_status not in LEAD_STATUSES:
            raise ValueError("Invalid lead status")

        # Get the allowed next statuses
        allowed_statuses = LEAD_STATUS_TRANSITIONS[self.status]

        # Check if the new status is allowed
        if new_status not in allowed_statuses:
            raise ValueError("Invalid lead status transition")

        # Update the lead status
        self.status = new_status