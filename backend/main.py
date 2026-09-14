from fastapi import FastAPI, HTTPException

from backend.database import get_technician


app = FastAPI()


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