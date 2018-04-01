import tkinter as tk
from datamodels import PatientData


def show_full_schedule():
    print("Showing Full Schedule")


def show_completed_visits():
    pass


def show_ongoing_visits():
    pass


def show_remaining_visits():
    pass


def add_new_patient():
    new_window = tk.Tk()
    new_window.title("Add New Patient")
    ents = make_form_add_patient(new_window)
    make_buttons_add_patient(new_window)

def add_to_day_schedule():
    pass
    

def make_form_add_patient(root):
    fields = ["Current Time", "Start Time", "End Time", "Procedure Duration", "Patient Type", "Patient Priority", "Patient Location"]
    entries = []
    for field in fields:
        row = tk.Frame(root)
        label = tk.Label(row, width = 15, text=field, anchor='w')
        entry = tk.Entry(row)
        row.pack(side='top', fill='x', padx=5, pady=5)
        label.pack(side='left')
        entry.pack(side='right', expand='YES', fill='x')
        entries.append((field, entry))
    return entries


def make_buttons_add_patient(new_window):
    row = tk.Frame(new_window)
    row.pack(side='top', fill='x', padx=5, pady=5)
    button1 = tk.Button(row, text="Cancel", fg="red", width=20, command=new_window.destroy)
    button1.pack(side='left')
    button2 = tk.Button(row, text="Confirm",fg="green", width=20, command=add_to_day_schedule)
    button2.pack(side='left')


def return_command_for_button(idx):
    if idx == 0:
        show_full_schedule()
    elif idx == 1:
        show_completed_visits()
    elif idx == 2:
        show_ongoing_visits()
    elif idx == 3:
        show_remaining_visits()
    elif idx == 4:
        add_new_patient()


button_labels = ["Show Full Schedule", "Show Completed Visits", "Show Ongoing Visits", "Show Remaining Visits", "Add New Patient"]

def make_buttons(root, button_labels):
    buttons = []
    for  idx, text in enumerate(button_labels):
        row = tk.Frame(root)
        row.pack(side='top', fill='x', padx=5, pady=5)
        button = tk.Button(row, text=text, width=20, command=lambda idx=idx: return_command_for_button(idx))
        button.pack(side='left')
        buttons.append(button)
    return buttons

if __name__ == '__main__':
   root = tk.Tk()
   root.title("Home Health Care Routing")
   buttons = make_buttons(root, button_labels)
#    ents = make_form(root, fields)
   root.mainloop()
