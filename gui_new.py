import tkinter as tk
from dorouting import RunSingleProblem
from datamodels import PatientData




class MainMenuScreen:

    def __init__(self):
        self.patient = PatientData()
        self.time = 0
        self.r_s_p = RunSingleProblem()
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.title("Home Health Care Routing")
        self.row = tk.Frame(self.root)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.entry = tk.Entry(self.row)
        self.problem_variable = tk.IntVar()
        self.minute_variable = tk.IntVar()
        self.minute_entry = tk.Entry(self.row)
        
        question = "Which problem would you like to run?"
        label = tk.Label(self.row, width = 30, text=question, anchor='w')
        label.pack(side='left')
        self.entry.pack(side='left', expand='YES')
        button = tk.Button(self.row, text="Solve", width=20, command=self.run_problem)
        button.pack(side='left')

        row = self.row
        row = tk.Frame(self.root)
        question = "Enter the current time to see current status on field:"
        label = tk.Label(row, width = 45, text=question, anchor='w')
        row.pack(side='top', fill='x', padx=5, pady=5)
        label.pack(side='left')
        self.minute_entry = tk.Entry(row)
        self.minute_entry.pack(side="left")

        row = tk.Frame(self.root)
        row.pack(side='top', fill='x', padx=5, pady=5)
        self.sfs_button = tk.Button(row, text="Show Full Schedule", width=20, command=self.show_full_schedule)
        self.sfs_button.pack(side='left')

        row = tk.Frame(self.root)
        row.pack(side='top', fill='x', padx=5, pady=5)
        self.scv_button = tk.Button(row, text="Show Completed Visits", width=20, command=self.show_completed_visits)
        self.scv_button.pack(side='left')

        row = tk.Frame(self.root)
        row.pack(side='top', fill='x', padx=5, pady=5)
        self.sov_button = tk.Button(row, text="Show Ongoing Visits", width=20, command=self.show_ongoing_visits)
        self.sov_button.pack(side='left')

        row = tk.Frame(self.root)
        row.pack(side='top', fill='x', padx=5, pady=5)
        self.srv_button = tk.Button(row, text="Show Remaining Visits", width=20, command=self.show_remaining_visits)
        self.srv_button.pack(side='left')

        row = tk.Frame(self.root)
        row.pack(side='top', fill='x', padx=5, pady=5)
        self.anp_button = tk.Button(row, text="Add New Patient", width=20, command=self.add_new_patient)
        self.anp_button.pack(side='left')
        # self.sfs_buttons.append(button)

        # self.add_patient_button = tk.Button()
        
    
    def main_screen(self, row):
        row = self.row
        question = "Which problem would you like to run?"
        label = tk.Label(row, width = 30, text=question, anchor='w')
        label.pack(side='left')
        self.entry.pack(side='left', expand='YES')
        button = tk.Button(row, text="Solve", width=20, command=self.run_problem)
        button.pack(side='left')
    
    def make_buttons(self, row):
        row = self.row
        row = tk.Frame(self.root)
        question = "Enter the current time to see current status on field:"
        label = tk.Label(row, width = 45, text=question, anchor='w')
        row.pack(side='top', fill='x', padx=5, pady=5)
        label.pack(side='left')
        self.minute_entry = tk.Entry(row)
        self.minute_entry.pack(side="left")
        button_labels = ["Show Full Schedule", "Show Completed Visits", "Show Ongoing Visits", "Show Remaining Visits", "Add New Patient"]
        buttons = []
        for  idx, text in enumerate(button_labels):
            row = tk.Frame(self.root)
            row.pack(side='top', fill='x', padx=5, pady=5)
            button = tk.Button(row, text=text, width=20, command=lambda idx=idx: self.return_command_for_button(idx))
            button.pack(side='left')
            buttons.append(button)
        return buttons

        self.add_patient_button = buttons[-1]
    
    def return_command_for_button(self, idx):
        if idx == 0:
            self.show_full_schedule()
        elif idx == 1:
            self.show_completed_visits()
        elif idx == 2:
            self.show_ongoing_visits()
        elif idx == 3:
            self.show_remaining_visits()
        elif idx == 4:
            self.add_new_patient()

    def display_screen(self):
        self.root.mainloop()
    
    def show_full_schedule(self):
        print("Showing Full Schedule")
        p_list = self.r_s_p.routing_problem.show_full_schedule()


    def show_completed_visits(self):
        self.minute_variable = int(self.minute_entry.get())
        p_list = self.r_s_p.routing_problem.show_completed_visits(self.minute_variable)
        # print(len(p_list))
        


    def show_ongoing_visits(self):
        self.minute_variable = int(self.minute_entry.get())
        p_list = self.r_s_p.routing_problem.show_ongoing_visits(self.minute_variable)
        print(len(p_list))


    def show_remaining_visits(self):
        self.minute_variable = int(self.minute_entry.get())
        p_list = self.r_s_p.routing_problem.show_remaining_visits(self.minute_variable)
        print(len(p_list))

    def run_problem(self):
        self.problem_variable = self.entry.get()
        self.r_s_p.run_problem(self.problem_variable)
        # self.make_buttons(self.row)


    def add_new_patient(self):
        self.anp_button.configure(state="disabled")
        add_new = AddNewPatient(self.root, self.r_s_p, self.patient, self.time)
        # add_new.display_screen()
        print("Came here")
        # self.r_s_p.routing_problem.add_new_patient(self.patient, self.time)
        

class AddNewPatient:

    def __init__(self, root, r_s_p, patient, time):

        self.patient = patient
        self.time = time
        self.r_s_p = r_s_p

        self.root = root
        # self.root.title("Add New Patient")
        self.root.resizable(width=False, height=False)
        self.row = tk.Frame(self.root)
        
        fields = ["Current Time", "Start Time", "End Time", "Procedure Duration", "Patient Type", "Patient Priority", "Patient Location"]
        self.current_time_label = tk.Label(self.row, width = 15, text=fields[0], anchor='w')
        self.current_time_entry = tk.Entry(self.row)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.current_time_label.pack(side='left')
        self.current_time_entry.pack(side='right', expand='YES', fill='x')
        self.current_time = tk.IntVar()

        self.row = tk.Frame(self.root)
        self.start_time_label = tk.Label(self.row, width = 15, text=fields[1], anchor='w')
        self.start_time_entry = tk.Entry(self.row)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.start_time_label.pack(side='left')
        self.start_time_entry.pack(side='right', expand='YES', fill='x')
        self.start_time = tk.IntVar()

        self.row = tk.Frame(self.root)
        self.end_time_label = tk.Label(self.row, width = 15, text=fields[2], anchor='w')
        self.end_time_entry = tk.Entry(self.row)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.end_time_label.pack(side='left')
        self.end_time_entry.pack(side='right', expand='YES', fill='x')
        self.end_time = tk.IntVar()

        self.row = tk.Frame(self.root)
        self.duration_label = tk.Label(self.row, width = 15, text=fields[3], anchor='w')
        self.duration_entry = tk.Entry(self.row)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.duration_label.pack(side='left')
        self.duration_entry.pack(side='right', expand='YES', fill='x')
        self.duration = tk.IntVar()

        self.row = tk.Frame(self.root)
        self.type_label = tk.Label(self.row, width = 15, text=fields[4], anchor='w')
        self.type_entry = tk.Entry(self.row)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.type_label.pack(side='left')
        self.type_entry.pack(side='right', expand='YES', fill='x')
        self.type = tk.IntVar()

        self.row = tk.Frame(self.root)
        self.priority_label = tk.Label(self.row, width = 15, text=fields[5], anchor='w')
        self.priority_entry = tk.Entry(self.row)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.priority_label.pack(side='left')
        self.priority_entry.pack(side='right', expand='YES', fill='x')
        self.priority = tk.IntVar()

        self.row = tk.Frame(self.root)
        self.location_label = tk.Label(self.row, width = 35, text=fields[6], anchor='w')
        self.location_x_entry = tk.Entry(self.row)
        self.location_y_entry = tk.Entry(self.row)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.location_label.pack(side='left')
        self.location_x_entry.pack(side='right', expand='YES', fill='x')
        self.location_y_entry.pack(side='right', expand='YES', fill='x')
        self.location_x = tk.IntVar()
        self.location_y = tk.IntVar()

        self.row = tk.Frame(self.root)
        self.row.pack(side='top', fill='x', padx=5, pady=5)
        self.cancel_button = tk.Button(self.row, text="Cancel", fg="red", width=20, command=self.root.destroy)
        self.cancel_button.pack(side='left')
        self.confirm_button = tk.Button(self.row, text="Confirm",fg="green", width=20, command=self.add_to_day_schedule)
        self.confirm_button.pack(side='right')
    
    def add_to_day_schedule(self):
        self.current_time = self.current_time_entry.get()
        self.start_time = self.start_time_entry.get()
        self.end_time = self.end_time_entry.get()
        self.duration = self.duration_entry.get()
        self.type = self.type_entry.get()
        self.priority = self.priority_entry.get()
        self.location_x = self.location_x_entry.get()
        self.location_y = self.location_y_entry.get()

        self.patient.window_open = int(self.start_time)
        self.patient.window_close = int(self.end_time)
        self.patient.care_duration = int(self.duration)
        self.patient.type_of_patient = int(self.type)
        self.patient.patient_priority = int(self.priority)
        self.patient.patient_location = (int(self.location_x), int(self.location_y))
        
        self.time = int(self.current_time)
        # self.root.destroy()
        self.r_s_p.routing_problem.add_new_patient(self.patient, self.time)
        

    
    def display_screen(self):
        self.root.mainloop()
        # return self.patient, self.time


main_screen = MainMenuScreen()
main_screen.display_screen()