from routing_mods import Routing
import readwrite
from datamodels import PatientData

class RunSingleProblem:

    def __init__(self):
        self.routing_problem = Routing()
        self.file_read = readwrite.ReadSingleFileData()
        self.csv_write = readwrite.WriteData()
    
    def run_problem(self, int):

        self.file_read.read_initialize_dayjob(int)
        self.routing_problem.job = self.file_read.day_job
        self.routing_problem.create_multiple_solutions()
        self.write_to_csv(int)
        
    def write_to_csv(self, int):
        self.csv_write.write_to_csv(self.routing_problem, self.routing_problem.solutions[0].crew_output, self.routing_problem.solutions[0].patients_left, int)

    def run_script(self):
        welcome_message = "*Home Health Care Routing*"
        print(welcome_message)
        prompt_for_problems = int(input("What do you want to solve?\n1. All problems\n2. Single problem\n"))
        if prompt_for_problems == 1:
            run_all_problems()
        elif prompt_for_problems == 2:
            choose_problem = int(input("Choose one of the 20 problems(1..20):"))
            self.run_problem(choose_problem)
            add_new_patient_prompt = input("Would you like to add new patient?\n Enter YES to proceed else NO to quit:\n")
            if add_new_patient_prompt == "YES":
                current_time = input("What is the current time?\nIt should be less that patient's earliest time you will enter.:\n")
                new_patient = PatientData()
                new_patient.create_a_patient()
                print(new_patient.data_as_string())
                self.routing_problem.add_new_patient(new_patient, int(current_time))
                self.write_to_csv(choose_problem)
            elif add_new_patient_prompt == "NO":
                pass
            else:
                add_new_patient_prompt = input("Would you like to add new patient?\n Enter YES to proceed else NO to quit:\n")
            
            print("Patient added:", add_new_patient_prompt)


class RunMultipleProblems:
    def __init__(self):
        self.routing_problems = []
        self.file_read = readwrite.ReadMultipleFileData()
        self.csv_write = readwrite.WriteData()
    
    def run_problems(self):

        self.file_read.read_initialize_multiple_dayjobs()
        for idx, day_job in enumerate(self.file_read.day_jobs):
            routing_problem = Routing()
            routing_problem.job = day_job
            routing_problem.create_multiple_solutions()
            self.csv_write.write_to_csv(routing_problem, routing_problem.solutions[0].crew_output, routing_problem.solutions[0].patients_left, idx)
        

# r_s_p = RunSingleProblem()
# r_s_p.run_script()