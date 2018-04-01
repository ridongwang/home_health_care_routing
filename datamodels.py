class PatientData:
    def __init__(self):
        self.index = 9999
        self.window_open = 0
        self.window_close = 0
        self.care_duration = 0
        self.patient_location = (0,0)
        self.patient_priority = 0
        self.type_of_patient = 0
        self.eta = 0
        self.etd = 0

    def data_as_string(self):
        return ",".join([str(self.index), str(self.window_open), str(self.window_close), str(self.care_duration), str(self.type_of_patient), str(self.patient_priority), str(self.patient_location[0]) + "x" + str(self.patient_location[1])])
    
    def create_a_patient(self):
        self.window_open = input("Earliest time patient can be attended?:\n")
        self.window_close = input("Latest time patient can be attended?:\n")
        self.care_duration = input("How long the visit will last?:\n")
        x = input("Patient's X coordinate:\n")
        y = input("Patient's Y coordinate:\n")
        self.patient_location = int(x),int(y)
        self.patient_priority = input("What is patient's priority?\n Choose between 1 to 3.\n")
        self.type_of_patient = input("What is the type of patient?\n Choose among 1001, 1004, 1005, 1007, 1009.\n")



class DayJobsInstance:
    def __init__(self):
        self.number_of_patients = 0
        self.number_of_crew = 0
        self.types_of_patient_count = 5
        self.length_of_visit = 20
        self.list_of_patients = []
        self.length_of_city = 20
        self.width_of_city = 20
        self.clinic_location = (0,0)
        self.work_minutes = 480   


class CrewAssignment:
    def __init__(self):
        self.crew_number = 0
        self.list_of_patients = []
        self.time_spent = 0
        self.vacant_times = []
        self.current_location = (0,0)
    
class ScheduleOutput:
    def __init__(self):
        self.crew_output = []
        self.patients_left = 0