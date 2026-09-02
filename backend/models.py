#Tech model
#Storing basic info about a technician

class Technician:

    # create a new technician
    def __init__(self, id, name, employee_number):

        # saveing the tech info
        self.id = id
        self.name = name
        self.employee_number = employee_number