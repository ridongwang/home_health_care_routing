import random
from operator import itemgetter
from math import sqrt

def read_data():
    with open('sample.txt', 'r') as file_object:
        data = file_object.readlines()
    file_object.close()
    # print(read_data)
    return data

# class PatientData(object):
#     def __init__(self):
#         self.window_open = 0
#         self.window_close = 0
#         self.care_duration = 0
#         self.patient_location = (0,0)
#         self.patient_priority = 0


class RoutingProblem:
    def __init__(self):
        self.crew = 0
        self.number_of_patients = 0
        self.caregiver_per_patient = 0
        self.average_speed = 40
        self.length_of_city = 20
        self.width_of_city = 20
        self.clinic_location = (0,0)
        self.work_minutes = 480
        self.list_patient_data = []
        self.patient_locations = []

    def initialize_from_file(self):
        data = read_data()
        def initialize_variables():
            for cnt, line in enumerate(data):
                # print("Line {}: {}".format(cnt, line))
                if cnt == 0:
                    self.crew = ''.join(line.split())
                if cnt == 1:
                    self.caregiver_per_patient = ''.join(line.split())
                if cnt == 2:
                    self.number_of_patients = ''.join(line.split())

        def initialize_patient_data():
            data = read_data()
            for cnt, line in enumerate(data):
                if cnt > 2 and cnt < 19:
                    line = line.strip('\n')
                    elem = line.split(" ")
                    self.list_patient_data.append(elem)
        
        def generate_patient_data():
            for i in range(20):
                # patient_data = PatientData()
                # patient_data.window_open = random.randint(0, 460)
                earliest_time = random.randint(0, 460)
                # patient_data.window_close = random.randint(patient_data.window_open + 20, 480)
                latest_time = random.randint(earliest_time + 20, 480)
                care_duration = 20
                patient_priority = 0
                patient_location = (random.randint(0, self.length_of_city),random.randint(0, self.width_of_city))
                
                self.list_patient_data.append([earliest_time, latest_time, care_duration, patient_priority, patient_location])

        def generate_random_location_on_map():
            for i in range(len(self.list_patient_data)):
                x = random.randint(0, self.length_of_city)
                y = random.randint(0, self.width_of_city)
                self.list_patient_data[i].append((x,y))
        
        initialize_variables()
        # initialize_patient_data()
        generate_patient_data()
        # generate_random_location_on_map()


routing = RoutingProblem()
routing.initialize_from_file()

# print(routing.crew)
# print(routing.number_of_patients)
# print(routing.caregiver_per_patient)
# print(routing.list_patient_data)     
# print(routing.patient_locations)  

class ScheduleMaker:
    routing = RoutingProblem()
    routing.initialize_from_file()

    routing.list_patient_data = sorted(routing.list_patient_data, key=itemgetter(0))
    print(routing.list_patient_data)
    locations_to_visit  = [i[4] for i in routing.list_patient_data]
    # print(locations_to_visit)
    crew_time_spent = {k:0 for k in range(int(routing.crew))}

    def pick_initial_earliest_start_times():
        early_start_list = sorted(routing.list_patient_data, key=itemgetter(0))
        return early_start_list[:int(routing.crew)]
    
    def pick_initial_nearest_locations():
        near_start_list = sorted(routing.list_patient_data, key=lambda k: sqrt((k[4][0] - routing.clinic_location[0])**2 + (k[4][1] - routing.clinic_location[1])**2))
        # print(near_start_list)
        locations_to_visit  = [i[4] for i in near_start_list]
        print(locations_to_visit)
        return near_start_list[:int(routing.crew)]
    
    def pick_initial_minimal_duration_time():
        minimal_duration_list = sorted(routing.list_patient_data, key=itemgetter(2))
        return minimal_duration_list[:int(routing.crew)]
    
    def distance( point1, point2):
        return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    
    def next_task_eligibility(self, assignment, crew_dict):
        output = []
        for k,v in crew_dict.items():
            dist = distance(assignment[4],v[-1])
            time_to_reach = dist/routing.average_speed * 60
            if crew_time_spent[k] + time_to_reach >= assignment[0]:
                output.append([True, dist, time_to_reach])
            else:
                output.append([False, dist, time_to_reach])
        
        return output 

    
    # print(crew_time_spent)

    def create_schedule(crew_dict):
        # crew_dict = {k:[v] for k,v in enumerate(pick_initial_earliest_start_times())}
        assigned_assignements = []
        for i in crew_dict.values():
            assigned_assignements.extend(i)
            
        rest_of_items  = [item for item in routing.list_patient_data if item not in assigned_assignements]
        if len(rest_of_items) != 0:
            rest_of_items = sorted(rest_of_items, key=itemgetter(0))
            output = self.next_task_eligibility(rest_of_items[0],crew_dict)
            least_time = min(x[2] for x in output) 
            for i in output:
                if i[0] is True and i[2] == least_time:
                    assigns = crew_dict[i]
                    assigns.append(rest_of_items[0])
                    crew_dict[i] = assigns
            create_schedule(crew_dict)
        return crew_dict
    
    # crew_dict = {k:[routing.clinic_location] for k in range(int(routing.crew))}
    crew_dict = {k:[v] for k,v in enumerate(pick_initial_earliest_start_times())}
    for k,v in crew_time_spent.items():
        data = crew_dict[k]
        print(data)
        distance_from_clinic = distance(data[-1][4], routing.clinic_location)
        print(distance_from_clinic)
        time_to_reach = (distance_from_clinic/routing.average_speed * 60) 
        print(time_to_reach)
        crew_time_spent[k] += time_to_reach + data[-1][2]
    
    print(crew_time_spent)

    sched = create_schedule(crew_dict)
    print(crew_dict)

           




        
        
    
    
        



    


    
    


    
