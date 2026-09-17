from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.database import (
    create_technician,
    get_technician,
    create_lead,
    get_lead,
    update_lead_status,
    get_leads_by_technician,
    get_rewards_by_technician,
)


app = FastAPI()


class TechnicianCreate(BaseModel):

    # Technician name
    name: str

    # Technician employee number
    employee_number: str


class LeadCreate(BaseModel):

    # Technician responsible for the lead
    technician_id: int

    # Customer name
    customer: str

    # Lead opportunity value
    opportunity: float

    # Current lead status
    status: str = "Created"

class LeadStatusUpdate(BaseModel):

    # Bew status for the lead
    status: str


@app.get("/health")
def health_check():

    # Check if the API is running
    return {
        "status": "ok",
        "message": "TechRewards API is running"
    }


@app.get("/technicians/{technician_id}")
def read_technician(technician_id: int):

    # Get the technician from the database
    technician = get_technician(technician_id)

    # Return an error if the technician does not exist
    if technician is None:
        raise HTTPException(
            status_code=404,
            detail="Technician not found"
        )

    # Convert the database result into JSON format
    return {
        "id": technician[0],
        "name": technician[1],
        "employee_number": technician[2]
    }


@app.post("/technicians")
def create_new_technician(technician_data: TechnicianCreate):

    # Create a new technician in the database
    technician_id = create_technician(
        technician_data.name,
        technician_data.employee_number
    )

    # Return the created technician ID
    return {
        "message": "Technician created successfully",
        "technician_id": technician_id
    }


@app.post("/leads")
def create_new_lead(lead_data: LeadCreate):

    # Create a new lead in the database
    lead_id = create_lead(
        lead_data.technician_id,
        lead_data.customer,
        lead_data.opportunity,
        lead_data.status
    )

    # Return the created lead ID
    return {
        "message": "Lead created successfully",
        "lead_id": lead_id
    }


@app.get("/leads/{lead_id}")
def read_lead(lead_id: int):

    # Get the lead from the database
    lead = get_lead(lead_id)

    # Return an error if the lead does not exist
    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    # Convert the database result into JSON format
    return {
        "id": lead[0],
        "technician_id": lead[1],
        "customer": lead[2],
        "opportunity": lead[3],
        "status": lead[4]
    }


@app.put("/leads/{lead_id}/status")
def change_lead_status(
    lead_id: int,
    status_data: LeadStatusUpdate
):

    # Update the lead status in the database
    try:
        update_lead_status(
            lead_id,
            status_data.status
        )

    # Return an error if the status change if invalid
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    # Get the updated lead
    lead = get_lead(lead_id)

    # Return an error if the lead does not exist
    if lead is None:
        raise HTTPException(
            status_code=404,
            details="Lead not found"
        )

    # Return the updated lead
    return {
        "message": "Lead status updated successfully",
        "lead_id": lead[0],
        "status": lead[4]
    }

@app.get("/technicians/{technician_id}/leads")
def read_technician_leads(technician_id: int):

    # Get all leads for this technician
    leads = get_leads_by_technician(technician_id)

    # Return an error if no leads exist
    if not leads:
        raise HTTPException(
            status_code=404,
            detail="No leads found for this technician"
        )

    # Return the leads
    return [
        {
            "id": lead[0],
            "technician_id": lead[1],
            "customer": lead[2],
            "opportunity": lead[3],
            "status": lead[4],
        }
        for lead in leads
    ]


@app.get("/technicians/{technician_id: int}/rewards")
def read_technician_rewards(technician_id: int):

    # Get all rewards for this technician
    rewards = get_rewards_by_technician(technician_id)

    # Return an error if no rewards exist
    if not rewards:
        raise HTTPException(
            status_code=404,
            detail="No rewards found for this technician"
        )

    # Return the rewards
    return [
        {
            "id": reward[0],
            "technician_id": reward[1],
            "reward_type": reward[2],
            "amount": reward[3],
            "description": reward[4],
        }
        for reward in rewards
    ]