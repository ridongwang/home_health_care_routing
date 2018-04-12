import random
from operator import itemgetter
from math import sqrt
from datetime import datetime
import pprint
import ast
import pathlib
from datamodels import *
import readwrite

class Routing:
    def __init__(self):
        self.job = DayJobsInstance()
        self.crew_list = []
        self.solutions = []
        self.sched_output = ScheduleOutput()
    
    def pick_initial_earliest_start_times(self, patient_list):
        """
        Find the first location for each crew where we have to reach the earliest.
        """
        early_start_list = sorted(patient_list, key=lambda x: x.window_open)
        return early_start_list[:int(self.job.number_of_crew)] 
    
    def pick_initial_nearest_locations(self, patient_list):
        """
        Find the first location for each crew which is nearest to the clinic.
        """
        near_start_list = sorted(patient_list, key=lambda k: sqrt((k.patient_location[0] - self.job.clinic_location[0])**2 + (k.patient_location[1] - self.job.clinic_location[1])**2))
        locations_to_visit  = [i.patient_location for i in near_start_list]
        return near_start_list[:int(self.job.number_of_crew)]

    def pick_initial_minimal_duration_time(self, patient_list):
        """
        Find the first location for each crew where we can finish the job the earliest.
        """
        minimal_duration_list = sorted(patient_list, key=lambda x: x.window_open + x.care_duration)
        
        return minimal_duration_list[:int(self.job.number_of_crew)]
    
    def pick_initial_high_priority_patients(self, patient_list):
        """
        Find the high priority patients which should be attended first.
        """
        high_priority_list = sorted(patient_list, key=lambda x: x.patient_priority)

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
        time_to_reach = (dist/60 * 60)

        return int(round(dist)),int(round(time_to_reach))

    def next_task_eligibility(self, assignment, crew_list):
        """
        Checks which crew can take the assignment.
        We return time to reach to assignment as well as distance in output.
        """
        output = []
        for i in crew_list:
            distance, time_to_reach = self.navigation_data(assignment.patient_location, i.current_location)
            eta_at_location = time_to_reach + i.time_spent
            if  eta_at_location <= int(assignment.window_open):
                output.append([True, i.crew_number, distance, time_to_reach, assignment.window_open, int(assignment.window_open) - time_to_reach])
            elif eta_at_location >= int(assignment.window_open) and eta_at_location <= int(assignment.window_close):
                output.append([True, i.crew_number, distance, time_to_reach, eta_at_location])

        return output

    def crew_patient_navigation_data(self, crew, patient):
        distance, time_to_reach = self.navigation_data(patient.patient_location, crew.current_location)
        eta_at_location = time_to_reach + crew.time_spent
        if  eta_at_location <= int(patient.window_open):
            return distance, patient.window_open
        elif eta_at_location >= int(patient.window_open) and eta_at_location <= int(patient.window_close):
            return distance, eta_at_location
        print("Will return nothing.")

    
    def create_schedule(self):
        """
        Creates the day scedule for the crew.
        """   
        assigned_assignements = []
        for i in self.crew_list:
            assigned_assignements.extend(i.list_of_patients)
        
        rest_of_items = []
        for item in self.job.list_of_patients:
            if item not in assigned_assignements:
                rest_of_items.append(item)

        
        if len(rest_of_items) != 0: 
            assignment = sorted(rest_of_items, key=lambda x: x.window_close)[0]
            output = self.next_task_eligibility(assignment, self.crew_list)
            if len(output) != 0:
                output_sorted = sorted(output, key=itemgetter(2))
                crew_to_assign = output_sorted[0][1]
                assignment.eta = int(output_sorted[0][4])
                assignment.etd = int(assignment.eta) + int(assignment.care_duration)
                crew = next((x for x in self.crew_list if x.crew_number == crew_to_assign), None)
                self.crew_list.remove(crew)
                crew.list_of_patients.append(assignment)
                crew.time_spent = assignment.etd
                self.crew_list.append(crew)

                self.create_schedule()
            else:
                # print("*" * 80, "\n", "*" * 80, "\nWe were not able to assign a task so stopped.\n", "*" * 80, "\n", "*" * 80)
                
                self.sched_output.crew_output = self.crew_list
                self.sched_output.patients_left = len(rest_of_items)
                
        elif not rest_of_items:
            self.sched_output.crew_output = self.crew_list
            self.sched_output.patients_left = 0

    def show_completed_visits(self, time):
        list_of_patients = []
        sched_output = self.solutions[0]
        for crew in sched_output.crew_output:
            for patient in crew.list_of_patients:
                if patient.etd < time:
                    list_of_patients.append(patient)
        
        return list_of_patients
    
    def show_ongoing_visits(self, time):
        list_of_patients = []
        sched_output = self.solutions[0]
        for crew in sched_output.crew_output:
            for patient in crew.list_of_patients:
                if patient.eta <= time and patient.etd >= time:
                    list_of_patients.append(patient)
        
        return list_of_patients
    
    def show_remaining_visits(self, time):
        list_of_patients = []
        sched_output = self.solutions[0]
        for crew in sched_output.crew_output:
            for patient in crew.list_of_patients:
                if patient.eta > time:
                    list_of_patients.append(patient)
        
        return list_of_patients
    
    def show_current_location_crew(self, time):
        list_current_loc = []
        sched_output = self.solutions[0]
        for crew in sched_output.crew_output:
            list_current_loc.append(crew.current_location)
        
        return list_current_loc
    
    def remove_remaining_visits(self, time):
        list_of_patients = []
        sched_output = self.solutions[0]
        for crew in sched_output.crew_output:
            for patient in crew.list_of_patients:
                # print(type(patient.eta),patient.eta)
                if int(patient.eta) > time:
                    crew.list_of_patients.remove(patient) 
            if not crew.list_of_patients:
                crew.current_location = (0,0)
        
    def add_new_patient(self, patient, time):
        self.remove_remaining_visits(time)
        self.job.list_of_patients.append(patient)
        self.create_schedule()
        self.solutions.insert(0, self.sched_output)
        self.sched_output = ScheduleOutput()
        # self.solutions = sorted(self.solutions, key=lambda x:x.patients_left)
        # self.solutions = sorted(self.solutions, key=lambda x:x.patients_left)
        for i in self.solutions:
            print(i, " has", i.patients_left, " patients left.\n")

    def check_patient_assigned(patient):
        assigned_assignements = []
        for i in self.solutions[0].crew_output:
            for crew in i:
                assigned_assignements.extend(j.list_of_patients)
        
        if patient in assigned_assignements:
            return True
        else:
            return False
        
         
    def initialize_crew(self):
        self.crew_list = []
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
            crew.current_location = val.patient_location
    
    def create_multiple_solutions(self):
        
        initial_assignments_combinations = [self.pick_initial_nearest_locations(self.job.list_of_patients), self.pick_initial_minimal_duration_time(self.job.list_of_patients), self.pick_initial_earliest_start_times(self.job.list_of_patients), self.pick_initial_high_priority_patients(self.job.list_of_patients)]
        for list in initial_assignments_combinations:
            self.initialize_crew()
            self.assign_first_jobs_crew(list)
            self.create_schedule()
            self.solutions.append(self.sched_output)
            self.sched_output = ScheduleOutput()
        
        
        self.solutions = sorted(self.solutions, key=lambda x:x.patients_left)
        for i in self.solutions:
            print(i, " has", i.patients_left, " patients left.\n")




def run_single_problem(int):

    routing_problem = Routing()
    routing_problem.job = read_initialize_dayjob(int)
    # routing_problem.initialize_crew()
    # routing_problem.assign_first_jobs_crew()
    # routing_problem.create_schedule()
    routing_problem.create_multiple_solutions()
    write_to_csv(routing_problem, routing_problem.solutions[0].crew_output, routing_problem.solutions[0].patients_left, 0)

def run_all_problems():
    day_jobs = read_initialize_multiple_dayjobs()
    for idx, i in enumerate(day_jobs):
        routing_problem = Routing()
        routing_problem.job = i
        print("Problem to solve is:\nNumber of patients-", routing_problem.job.number_of_patients, "Number of crew-", routing_problem.job.number_of_crew)
        # routing_problem.initialize_crew()
        # routing_problem.assign_first_jobs_crew()
        # routing_problem.create_schedule()
        # write_to_csv(routing_problem, routing_problem.sched_output.crew_output, routing_problem.sched_output.patients_left, idx)
        routing_problem.create_multiple_solutions()
        write_to_csv(routing_problem, routing_problem.solutions[0].crew_output, routing_problem.solutions[0].patients_left, idx)

# run_all_problems()

def run_script():
    welcome_message = "*Home Health Care Routing*"
    print(welcome_message)
    prompt_for_problems = int(input("What do you want to solve?\n1. All problems\n2. Single problem\n"))
    if prompt_for_problems == 1:
        run_all_problems()
    elif prompt_for_problems == 2:
        choose_problem = int(input("Choose one of the 20 problems(1..20):"))
        run_single_problem(choose_problem)
        add_new_patient_prompt = input("Would you like to add new patient?\n Enter YES to proceed else NO to quit:\n")
        if add_new_patient_prompt == "YES":
            current_time = input("What is the current time?\nIt should be less that patient's earliest time you will enter.:\n")
            new_patient = PatientData()
            new_patient.create_a_patient()
            print(new_patient.data_as_string())
            
        elif add_new_patient_prompt == "NO":
            pass
        else:
            add_new_patient_prompt = input("Would you like to add new patient?\n Enter YES to proceed else NO to quit:\n")
        
        print("Patient added:", add_new_patient_prompt)

# run_script()

