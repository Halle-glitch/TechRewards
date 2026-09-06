from backend.models import Technician, Lead

# create a technician
technician = Technician(1, "Miguel", "RT001")


# show tech info
print(technician.name)
print(technician.employee_number)

lead = Lead(1, 1111, "Cumberland", "Spray", "Created")

print(lead.status)

lead.update_status("Sent")

print(lead.status)