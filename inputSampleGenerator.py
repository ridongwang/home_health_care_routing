import random
from math import sqrt
import pprint

class PatientData:
    def __init__(self):
        self.index = 9999
        self.window_open = 0
        self.window_close = 0
        self.care_duration = 0
        self.patient_location = (0,0)
        self.patient_priority = 0
        self.type_of_patient = 0

    def data_as_string(self):
        return " ".join([str(self.index), str(self.window_open), str(self.window_close), str(self.care_duration), str(self.type_of_patient), str(self.patient_priority)])


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
    
    def create_patient_data(self, count):
        length_of_visit_choices = [15, 20, 30, 45, 60, self.length_of_visit]
        
        for i in range(0, count):
            patient = PatientData()
            patient.index = i
            patient.window_open = random.randint(0, 460)
            patient.care_duration = random.choice(length_of_visit_choices)
            patient.window_close =  random.randint(patient.window_open, 480)
            patient.patient_location = self.generate_random_location_on_map()
            patient.patient_priority = random.choice([1,2,3])
            patient.type_of_patient = random.choice([1001, 1004, 1005, 1007, 1009])
            # print(patient.data_as_string())
            self.list_of_patients.append(patient)

    def generate_random_location_on_map(self):
        x = random.randint(0, self.length_of_city)
        y = random.randint(0, self.width_of_city)
        return (x,y)
    
    def distance(self, point1, point2):
        """
        Find the distance between two locations.
        """
        dist = int(sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))
        # print("Distance between two location is ", dist)
        return dist

    def generate_distance_matrix(self):
        matrix = [[] for i in range(0, len(self.list_of_patients))]
        for i in range(0, len(self.list_of_patients)):
            for j in range(0, len(self.list_of_patients)):
                patient1 = PatientData()
                patient1 = self.list_of_patients[i]
                patient2 = PatientData()
                patient2 = self.list_of_patients[j]

                distance = self.distance(patient1.patient_location, patient2.patient_location)
                matrix[i].append(distance)
        
        return matrix

monday = DayJobsInstance()
monday.number_of_patients = 30
monday.number_of_crew = 5
monday.create_patient_data(monday.number_of_patients)
distance_matrix = monday.generate_distance_matrix()
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(distance_matrix)

number_of_patients = [10, 20, 30, 40 ,50]
number_of_crew = [5, 10, 15, 20]

list_of_instances = []
matrices = []
for idx, val in enumerate(number_of_patients):
    for jdx, second_val in enumerate(number_of_crew):
        job_instance = DayJobsInstance()
        # print(number_of_patients[i])
        job_instance.number_of_patients = number_of_patients[idx]
        print(job_instance.number_of_patients)
        job_instance.number_of_crew = number_of_crew[jdx]
        job_instance.create_patient_data(job_instance.number_of_patients)
        # for k in job_instance.list_of_patients:
        #     print(k.data_as_string())
        print(len(job_instance.list_of_patients))
        distance_matrix = job_instance.generate_distance_matrix()
        list_of_instances.append(job_instance)
        matrices.append(distance_matrix)

print(len(list_of_instances))

for idx, val in enumerate(list_of_instances):
    filename = "instances_" + str(idx) + ".txt"
    download_dir = filename 
    text = open(download_dir, "w")
    # job = DayJobsInstance()
    job = list_of_instances[idx]
    print(type(list_of_instances[idx]))
    patients = job.list_of_patients
    print(len(patients))
    lines = [str(job.number_of_crew), str(job.number_of_patients), str(job.types_of_patient_count)]
    for i in patients:
        patient = PatientData()
        patient = i
        line = " ".join([str(patient.index), str(patient.window_open), str(patient.window_close), str(patient.care_duration), str(patient.type_of_patient), str(patient.patient_priority), str(patient.patient_location)])
        # print("P Data", line)
        lines.append(line)
    
    text.write('\n'.join(lines))


    text.close()









