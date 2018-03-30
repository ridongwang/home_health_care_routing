import random
from operator import itemgetter
from math import sqrt
from datetime import datetime
import pprint
import ast
import pathlib

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

class Routing:
    def __init__(self):
        self.job = DayJobsInstance()
        self.crew_list = []
        self.solutions = []
        self.sched_output = ScheduleOutput()
    
    def pick_initial_earliest_start_times():
        """
        Find the first location for each crew where we have to reach the earliest.
        """
        early_start_list = sorted(self.job.list_of_patients, key=lambda x: x.window_open)
        return early_start_list[:int(self.job.number_of_crew)]
    
    def pick_initial_nearest_locations(self):
        """
        Find the first location for each crew which is nearest to the clinic.
        """
        near_start_list = sorted(self.job.list_of_patients, key=lambda k: sqrt((k.patient_location[0] - self.job.clinic_location[0])**2 + (k.patient_location[1] - self.job.clinic_location[1])**2))
        locations_to_visit  = [i.patient_location for i in near_start_list]
        # print("Locations picked to visit as as follows ", locations_to_visit)
        return near_start_list[:int(self.job.number_of_crew)]

    def pick_initial_minimal_duration_time():
        """
        Find the first location for each crew where we can finish the job the earliest.
        """
        minimal_duration_list = sorted(self.job.list_of_patients, key=lambda x: x.window_open + x.care_duration)
        
        return minimal_duration_list[:int(self.job.number_of_crew)]
    
    def pick_high_priority_patients():
        """
        Find the high priority patients which should be attended first.
        """
        high_priority_list = sorted(self.job.list_of_patients, key=lambda x: x.patient_priority)

        return high_priority_list[:int(self.job.number_of_crew)]
    
    def distance(self, point1, point2):
        """
        Find the distance between two locations.
        """
        dist = int(round(sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)))
        
        return dist
    
    def navigation_data(self, point1, point2):
        """
        Returns distance, time to reach between two locations.
        """
        dist = int(sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))
        time_to_reach = (dist/50 * 60)

        return int(round(dist)),int(round(time_to_reach))

    def next_task_eligibility(self, assignment, crew_list):
        """
        Checks which crew can take the assignment.
        We return time to reach to assignment as well as distance in output.
        """
        output = []
        for i in crew_list:
            distance, time_to_reach = self.navigation_data(assignment.patient_location, i.list_of_patients[-1].patient_location)
            eta_at_location = time_to_reach + i.time_spent
            if  eta_at_location <= int(assignment.window_open):
                # print("Next Task Eligibility, ELIGIBLE WITH REST AND EARLIEST ON WINDOW")
                # print(assignment.window_open)
                output.append([True, i.crew_number, distance, time_to_reach, assignment.window_open, int(assignment.window_open) - time_to_reach])
            elif eta_at_location >= int(assignment.window_open) and eta_at_location <= int(assignment.window_close):
                # print("Next Task Eligibility, ELIGIBLE WITHIN WINDOW")
                # print(eta_at_location)
                output.append([True, i.crew_number, distance, time_to_reach, eta_at_location])

        return output

    def crew_patient_navigation_data(self, crew, patient):
        distance, time_to_reach = self.navigation_data(patient.patient_location, crew.current_location)
        eta_at_location = time_to_reach + crew.time_spent
        if  eta_at_location <= int(patient.window_open):
            return distance, patient.window_open
        elif eta_at_location >= int(patient.window_open) and eta_at_location <= int(patient.window_close):
            return distance, eta_at_location

    
    def create_schedule(self):
        """
        Creates the day scedule for the crew.
        """   
        # sched_output = ScheduleOutput()
        assigned_assignements = []
        for i in self.crew_list:
            assigned_assignements.extend(i.list_of_patients)
        
        rest_of_items = []
        for item in self.job.list_of_patients:
            if item not in assigned_assignements:
                rest_of_items.append(item)
        
        # print("Rest of the items are:", len(rest_of_items))
        
        if len(rest_of_items) != 0:
            assignment = sorted(rest_of_items, key=lambda x: x.window_open)[0]
            # print("\nNext assignment to be taken ", assignment)
            output = self.next_task_eligibility(assignment, self.crew_list)
            if len(output) != 0:
                output_sorted = sorted(output, key=itemgetter(2))
                crew_to_assign = output_sorted[0][1]
                assignment.eta = output_sorted[0][4]
                # print("Crew ETA given", assignment.eta)
                assignment.etd = int(assignment.eta) + int(assignment.care_duration)
                crew = next((x for x in self.crew_list if x.crew_number == crew_to_assign), None)
                self.crew_list.remove(crew)
                crew.list_of_patients.append(assignment)
                crew.time_spent = assignment.etd
                self.crew_list.append(crew)

                self.create_schedule()
            else:
                print("*" * 80, "\n", "*" * 80, "\nWe were not able to assign a task so stopped.\n", "*" * 80, "\n", "*" * 80)
                
                self.sched_output.crew_output = self.crew_list
                self.sched_output.patients_left = len(rest_of_items)
                print("Visits left", self.sched_output.patients_left)
                
        elif not rest_of_items:
            print("Fully solved.")

            self.sched_output.crew_output = self.crew_list
            self.sched_output.patients_left = 0
        
        # print("Visits Left before returning:", self.sched_output.patients_left)
        # return self.sched_output

    
    def initialize_crew(self):
        for i in range(1, int(self.job.number_of_crew) + 1):
            crew = CrewAssignment()
            crew.crew_number = i
            self.crew_list.append(crew)

    def assign_first_jobs_crew(self, list):

        for idx,val in enumerate(list):
            crew = self.crew_list[idx]
            dist, time = self.crew_patient_navigation_data(crew, val)
            val.eta = time
            val.etd = int(val.eta) + int(val.care_duration)
            crew.time_spent = val.etd
            crew.list_of_patients.append(val)
    
    def create_multiple_solutions(self):

        self.initialize_crew()
        initial_assignments_combinations = [self.pick_initial_nearest_locations(), self.pick_initial_minimal_duration_time(), self.pick_initial_earliest_start_times(), self.pick_high_priority_patients()]
        for list in initial_assignments_combinations:
            self.assign_first_jobs_crew(list)
            self.create_schedule()


def read_initialize_dayjob():
    datasets = []
    def read_for_simulation():
        for i in range(0, 20):
            filename = "instances_" + str(i) + '.txt'
            with open(filename, 'r') as file_object:
                datasets.append(list(file_object))
            file_object.close()

    def read_single_file():
        filename = "instances_0.txt"
        with open(filename, 'r') as file_object:
            datasets.append(list(file_object))
        file_object.close()

    read_single_file()
    day_job = DayJobsInstance()
    for i in datasets:        
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
            # loc_tuple = ast.literal_eval(lit)
            datum.patient_location = ast.literal_eval(lit)
            day_job.list_of_patients.append(datum)
    
    return day_job

def read_initialize_multiple_dayjobs():
    datasets = []
    def read_for_simulation():
        for i in range(0, 20):
            filename = "instances_" + str(i) + '.txt'
            with open(filename, 'r') as file_object:
                datasets.append(list(file_object))
            file_object.close()
    
    read_for_simulation()
    dayjobs = []
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
            # loc_tuple = ast.literal_eval(lit)
            datum.patient_location = ast.literal_eval(lit)
            day_job.list_of_patients.append(datum)
        
        dayjobs.append(day_job)
    
    return dayjobs


def write_to_csv(routing_problem, routing_solution, patients_left, i):
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
            # print(string_to_write)
            csv.write(string_to_write)


# read_initialize_data()
def run_single_problem():

    routing_problem = Routing()
    routing_problem.job = read_initialize_dayjob()
    routing_problem.initialize_crew()
    routing_problem.assign_first_jobs_crew()
    routing_problem.create_schedule()
    write_to_csv(routing_problem, routing_problem.sched_output.crew_output, routing_problem.sched_output.patients_left, 0)

def run_all_problems():
    day_jobs = read_initialize_multiple_dayjobs()
    for idx, i in enumerate(day_jobs):
        routing_problem = Routing()
        routing_problem.job = i
        print("Problem to solve is:\nNumber of patients-", routing_problem.job.number_of_patients, "Number of crew-", routing_problem.job.number_of_crew)
        routing_problem.initialize_crew()
        routing_problem.assign_first_jobs_crew()
        routing_problem.create_schedule()
        write_to_csv(routing_problem, routing_problem.sched_output.crew_output, routing_problem.sched_output.patients_left, idx)

run_all_problems()