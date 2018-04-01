from datamodels import DayJobsInstance
from datamodels import PatientData
import ast
from datetime import datetime

class ReadSingleFileData:

    def __init__(self):
        self.day_job =  DayJobsInstance()

    def read_initialize_dayjob(self, int):
        datasets = []
        def read_single_file():
            filename = "instances_" + str(int) + ".txt"
            with open(filename, 'r') as file_object:
                datasets.append(list(file_object))
            file_object.close()


        read_single_file()
        def create_day_job_instance():
            # day_job = DayJobsInstance()
            for i in datasets:        
                self.day_job.number_of_crew = i[0]
                self.day_job.number_of_patients = i[1]
                for j in range(3, len(i)):
                    datum = PatientData()
                    line = i[j].rsplit(" ", 2)
                    part_data = line[0].split(" ")
                    del line[0]
                    datum.index = part_data[0]
                    datum.window_open = part_data[1]
                    datum.window_close = part_data[2]
                    datum.care_duration = part_data[3]
                    datum.type_of_patient = part_data[4]
                    datum.patient_priority = part_data[5]
                    lit = " ".join(line)
                    datum.patient_location = ast.literal_eval(lit)
                    self.day_job.list_of_patients.append(datum)
        
        create_day_job_instance()

        
class ReadMultipleFileData:

    def __init__(self):
        self.day_jobs =  []

    def read_initialize_multiple_dayjobs(self):
        datasets = []
        def read_for_simulation():
            for i in range(0, 20):
                filename = "instances_" + str(i) + '.txt'
                with open(filename, 'r') as file_object:
                    datasets.append(list(file_object))
                file_object.close()
        
        read_for_simulation()
        for i in datasets:
            day_job = DayJobsInstance()        
            day_job.number_of_crew = i[0]
            day_job.number_of_patients = i[1]
            for j in range(3, len(i)):
                datum = PatientData()
                line = i[j].rsplit(" ", 2)
                part_data = line[0].split(" ")
                del line[0]
                datum.index = part_data[0]
                datum.window_open = part_data[1]
                datum.window_close = part_data[2]
                datum.care_duration = part_data[3]
                datum.type_of_patient = part_data[4]
                datum.patient_priority = part_data[5]
                lit = " ".join(line)
                datum.patient_location = ast.literal_eval(lit)
                day_job.list_of_patients.append(datum)
            
            self.day_jobs.append(day_job)


class WriteData:

    @classmethod
    def write_to_csv(self, routing_problem, routing_solution, patients_left, i):
        time = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = "patientData_" + str(i) + "_"+ time + ".csv"
        download_dir = filename 
        csv = open(download_dir, "w") 

        header_info = "Number of Calls, Visits Left, Crew Count\n"
        csv.write(header_info)
        
        line = str(len(routing_problem.job.list_of_patients)) + "," + str(patients_left) + "," + str(routing_problem.job.number_of_crew) + "\n"
        print(header_info + "\n" + line)
        csv.write(line)

        column_title_row = "Patient Index, Start Time, End Time, Visit Duration, Patient Type, Priority, Location, Crew, Expected Time of Arrival\n"
        csv.write(column_title_row)

        for item in routing_solution:
            for patient in item.list_of_patients:
                string_to_write = patient.data_as_string()
                string_to_write = string_to_write + "," + str(item.crew_number) + "," + str(patient.eta) + "\n"
                csv.write(string_to_write)