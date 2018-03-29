import random
from operator import itemgetter
from math import sqrt
from datetime import datetime
import pprint
import ast

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
    
    def distance(self, point1, point2):
        """
        Find the distance between two locations.
        """
        dist = int(sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))
        # print("Distance between two location is ", dist)
        return dist

class Routing:
    def __init__(self):
        self.job = DayJobsInstance()
        self.solutions = []
    
    def pick_initial_earliest_start_times():
        """
        Find the first location for each crew where we have to reach the earliest.
        """
        early_start_list = sorted(self.job.list_of_patients, key=itemgetter(0))
        return early_start_list[:int(self.job.number_of_crew)]
    
    def pick_initial_nearest_locations():
        """
        Find the first location for each crew which is nearest to the clinic.
        """
        near_start_list = sorted(self.job.list_of_patients, key=lambda k: sqrt((k[6][0] - routing.clinic_location[0])**2 + (k[6][1] - routing.clinic_location[1])**2))
        locations_to_visit  = [i.patient_location for i in near_start_list]
        print("Locations picked to visit as as follows ", locations_to_visit)
        return near_start_list[:int(self.job.number_of_crew)]

    def pick_initial_minimal_duration_time():
        """
        Find the first location for each crew where we can finish the job the earliest.
        """
        minimal_duration_list = sorted(self.job.list_of_patients, key=lambda x: x.window_open)
        return minimal_duration_list[:int(self.job.number_of_crew)]
    
    def next_task_eligibility(assignment, crew_dict):
        """
        Checks which crew can take the assignment.
        We return time to reach to assignment as well as distance in output.
        """
        output = {}
        for k,v in crew_dict.items():
            
            dist = 0
            if len(v[-1]) == 2:
                print("WITH ADDITIONAL DATA Current crew location is ", v[-1], " and next assigment is at ", assignment[4])
                print("Point being passed is ", v[-1][0][4])
                dist = int(distance(assignment[4],v[-1][0][4]))
            else:
                print("NORMAL DATA Current crew location is ", v[-1], " and next assigment is at now ", assignment[4])
                print("Point being passed is ", v[-1][4])
                dist = int(distance(assignment[4],v[-1][4]))
                
            
            time_to_reach = int(dist/routing.average_speed * 60)
            print("Crew: ", k, "Distance: ", dist, "Time to reach: ", time_to_reach)
            print("Current time spent by crew: ", crew_time_spent[k], "ETA at this assignment: ", crew_time_spent[k] + time_to_reach)
            print("Assignment's start time:", assignment[0])
            if crew_time_spent[k] + time_to_reach >= routing.work_minutes:
                output[k] = [False, dist, time_to_reach]
            else:
                if crew_time_spent[k] + time_to_reach <= assignment[0]:
                    print("Next Task Eligibility, ELIGIBLE WITH REST AND EARLIEST ON WINDOW")
                    # output.append([True, dist, time_to_reach, assignment[0] - time_to_reach])
                    output[k] = [True, dist, time_to_reach, int(assignment[0] - time_to_reach), assignment[0]]
                elif crew_time_spent[k] + time_to_reach >= assignment[1]:
                    print("Next Task Eligibility, NOT ELEGIBLE")
                    # output.append([False, dist, time_to_reach])
                    output[k] = [False, dist, time_to_reach, crew_time_spent[k] + time_to_reach]
                elif crew_time_spent[k] + time_to_reach >= assignment[0] and crew_time_spent[k] + time_to_reach <= assignment[1] - assignment[2]:
                    print("Next Task Eligibility, ELIGIBLE WITHIN WINDOW")
                    # output.append([True, dist, time_to_reach])
                    output[k] = [True, dist, time_to_reach, int(crew_time_spent[k] + time_to_reach)]
                # elif crew_time_spent[k] + time_to_reach >= assignment[0] and crew_time_spent[k] + time_to_reach <= assignment[0] - assignment[2]:
                #     print("Next Task Eligibility, Condition Four Satisfied")
                #     output.append([True, dist, time_to_reach])

            

        return output 
    
    def create_schedule(self, crew_dict):
        """
        Creates the day scedule for the crew based on the crew_dict passed.
        """   
        assigned_assignements = []
        for i in crew_dict.values():
            assigned_assignements.append(i)

        
        rest_of_items = []
        # rest_of_items  = [item for item in routing.list_patient_data if item not in assigned_assignements]
        print("Assigned assignment list is ", assigned_assignements)
        for item in self.job.list_of_patients:
            if item not in assigned_assignements:
                rest_of_items.append(item)
        
        print("Rest of the items are as follows:", rest_of_items)
        
        if len(rest_of_items) != 0:
            rest_of_items = sorted(rest_of_items, key=itemgetter(0))
            print("\nNext assignment to be taken ", rest_of_items[0])
            # output_unsorted = next_task_eligibility(rest_of_items[0],crew_dict)
            output = next_task_eligibility(rest_of_items[0],crew_dict)
            # print("\nTask eligibility for each crew is ", output_unsorted)
            output_unsorted = output.values()
            # least_time = min(x[2] for x in output_unsorted) 
            output_sorted = sorted(output_unsorted, key=itemgetter(2))
            task_assigned_flag = False
            for val in output_sorted:
                if val[0] is True:
                    crew = list(output.keys())[list(output.values()).index(val)]
                    assigns = crew_dict.get(crew)
                    data_to_add = []
                    data_to_add.append(rest_of_items[0])
                    data_to_add.append([val[1], val[2], val[3]])
                    assigns.append(data_to_add)
                    crew_dict[crew] = assigns
                    task_assigned_flag = True
                    print(crew_dict)
                    if len(val) == 5:
                        print("Starting after a rest and finishing the assignment ", val[4] + val[2] + rest_of_items[0][-3])
                        print("Assignment duration ", rest_of_items[0][-3])
                        crew_time_spent[crew] = val[4] + val[2] + rest_of_items[0][-3]
                    else:
                        print("Generally starting and finishing the assignment ", crew_time_spent[crew] + val[2] + rest_of_items[0][-2])
                        crew_time_spent[crew] = crew_time_spent[crew] + val[2] + rest_of_items[0][-2]
                    print("Crew time after this assignment ",crew_time_spent[crew])
                    break
                elif val[0] is False:
                    continue
            

        
            if task_assigned_flag == True:
                create_schedule(crew_dict)
            else:
                print("*" * 80, "\n", "*" * 80, "\nWe were not able to assign a task so the script stopped.\n", "*" * 80, "\n", "*" * 80)
                # return [crew_dict, rest_of_items]

        return crew_dict

def read_data():
    datasets = []
    def read_for_simulation():
        for i in range(0, 20):
            filename = "instances_" + str(i) + '.txt'
            with open(filename, 'r') as file_object:
                datasets.append(list(file_object))
            file_object.close()

    def read_single_file():
        filename = "instances_19.txt"
        with open(filename, 'r') as file_object:
            datasets.append(list(file_object))
        file_object.close()

    read_single_file()
    day_job = DayJobsInstance()
    for i in datasets:        
        day_job.number_of_crew = i[0]
        day_job.number_of_patients = i[1]
        for j in range(3, len(i)):
            line = i[j].rsplit(" ", 2)
            datum = line[0].split(" ")
            del line[0]
            lit = " ".join(line)
            loc_tuple = ast.literal_eval(lit)
            datum.append(loc_tuple)
            day_job.list_of_patients.append(datum)

    for i in day_job.list_of_patients:
        print(i)

    


read_data()