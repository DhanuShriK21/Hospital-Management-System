from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id TEXT,
    name TEXT,
    age TEXT,
    disease TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    patient TEXT,
    doctor TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()

# ---------------- WINDOW ---------------- #

root = Tk()
root.title("Advanced Hospital Management System")
root.geometry("1200x700")
root.configure(bg="lightblue")

# ---------------- FUNCTIONS ---------------- #

def add_patient():

    pid = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    disease = disease_entry.get()

    if pid == "" or name == "" or age == "" or disease == "":
        messagebox.showerror("Error", "All Fields Required")
        return

    cursor.execute(
        "INSERT INTO patients VALUES (?, ?, ?, ?)",
        (pid, name, age, disease)
    )

    conn.commit()

    patient_table.insert(
        "",
        END,
        values=(pid, aname, age, disease)
    )

    messagebox.showinfo(
        "Success",
        "Patient Added Successfully"
    )

    clear_patient_fields()


def show_patients():

    for row in patient_table.get_children():
        patient_table.delete(row)

    cursor.execute("SELECT * FROM patients")

    rows = cursor.fetchall()

    for row in rows:
        patient_table.insert("", END, values=row)


def delete_patient():

    selected = patient_table.selection()

    if not selected:
        messagebox.showerror("Error", "Select Patient")
        return

    values = patient_table.item(selected, "values")

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (values[0],)
    )

    conn.commit()

    patient_table.delete(selected)

    messagebox.showinfo(
        "Deleted",
        "Patient Deleted Successfully"
    )


def search_patient():

    search_id = search_entry.get()

    for row in patient_table.get_children():
        patient_table.delete(row)

    cursor.execute(
        "SELECT * FROM patients WHERE id=?",
        (search_id,)
    )

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            patient_table.insert("", END, values=row)
    else:
        messagebox.showerror(
            "Not Found",
            "Patient Not Found"
        )


def update_patient():

    selected = patient_table.selection()

    if not selected:
        messagebox.showerror("Error", "Select Patient")
        return

    pid = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    disease = disease_entry.get()

    cursor.execute("""
    UPDATE patients
    SET name=?, age=?, disease=?
    WHERE id=?
    """, (name, age, disease, pid))

    conn.commit()

    show_patients()

    messagebox.showinfo(
        "Updated",
        "Patient Updated Successfully"
    )


def clear_patient_fields():

    id_entry.delete(0, END)
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    disease_entry.delete(0, END)


# ---------------- APPOINTMENT ---------------- #

def book_appointment():

    patient = patient_entry.get()
    doctor = doctor_entry.get()
    date = date_entry.get()
    time = time_entry.get()

    if patient == "" or doctor == "" or date == "" or time == "":
        messagebox.showerror(
            "Error",
            "All Appointment Fields Required"
        )
        return

    cursor.execute("""
    INSERT INTO appointments VALUES (?, ?, ?, ?)
    """, (patient, doctor, date, time))

    conn.commit()

    appointment_table.insert(
        "",
        END,
        values=(patient, doctor, date, time)
    )

    messagebox.showinfo(
        "Success",
        "Appointment Booked Successfully"
    )

    patient_entry.delete(0, END)
    doctor_entry.delete(0, END)
    date_entry.delete(0, END)
    time_entry.delete(0, END)


def show_appointments():

    for row in appointment_table.get_children():
        appointment_table.delete(row)

    cursor.execute("SELECT * FROM appointments")

    rows = cursor.fetchall()

    for row in rows:
        appointment_table.insert("", END, values=row)


# ---------------- TITLE ---------------- #

title = Label(
    root,
    text="ADVANCED HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold"),
    bg="lightblue",
    fg="darkblue"
)

title.pack(pady=10)

# ---------------- PATIENT FORM ---------------- #

form_frame = Frame(root, bg="lightblue")
form_frame.pack()

Label(
    form_frame,
    text="Patient ID",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=0, column=0, padx=10, pady=10)

id_entry = Entry(form_frame, font=("Arial", 12))
id_entry.grid(row=0, column=1)

Label(
    form_frame,
    text="Patient Name",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=1, column=0, padx=10, pady=10)

name_entry = Entry(form_frame, font=("Arial", 12))
name_entry.grid(row=1, column=1)

Label(
    form_frame,
    text="Age",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=2, column=0, padx=10, pady=10)

age_entry = Entry(form_frame, font=("Arial", 12))
age_entry.grid(row=2, column=1)

Label(
    form_frame,
    text="Disease",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=3, column=0, padx=10, pady=10)

disease_entry = Entry(form_frame, font=("Arial", 12))
disease_entry.grid(row=3, column=1)

# ---------------- BUTTONS ---------------- #

button_frame = Frame(root, bg="lightblue")
button_frame.pack(pady=10)

Button(
    button_frame,
    text="Add Patient",
    font=("Arial", 12),
    bg="green",
    fg="white",
    width=15,
    command=add_patient
).grid(row=0, column=0, padx=10)

Button(
    button_frame,
    text="Update Patient",
    font=("Arial", 12),
    bg="orange",
    fg="white",
    width=15,
    command=update_patient
).grid(row=0, column=1, padx=10)

Button(
    button_frame,
    text="Delete Patient",
    font=("Arial", 12),
    bg="red",
    fg="white",
    width=15,
    command=delete_patient
).grid(row=0, column=2, padx=10)

Button(
    button_frame,
    text="Show Patients",
    font=("Arial", 12),
    bg="blue",
    fg="white",
    width=15,
    command=show_patients
).grid(row=0, column=3, padx=10)

# ---------------- SEARCH ---------------- #

search_frame = Frame(root, bg="lightblue")
search_frame.pack(pady=10)

Label(
    search_frame,
    text="Search Patient ID",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=0, column=0)

search_entry = Entry(search_frame, font=("Arial", 12))
search_entry.grid(row=0, column=1, padx=10)

Button(
    search_frame,
    text="Search",
    font=("Arial", 12),
    bg="purple",
    fg="white",
    command=search_patient
).grid(row=0, column=2)

# ---------------- PATIENT TABLE ---------------- #

table_frame = Frame(root)
table_frame.pack(pady=20)

patient_table = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Age", "Disease"),
    show="headings",
    height=8
)

patient_table.heading("ID", text="Patient ID")
patient_table.heading("Name", text="Patient Name")
patient_table.heading("Age", text="Age")
patient_table.heading("Disease", text="Disease")

patient_table.column("ID", width=150)
patient_table.column("Name", width=250)
patient_table.column("Age", width=100)
patient_table.column("Disease", width=250)

patient_table.pack()

# ---------------- APPOINTMENT SECTION ---------------- #

appointment_title = Label(
    root,
    text="Appointment Booking",
    font=("Arial", 20, "bold"),
    bg="lightblue",
    fg="darkgreen"
)

appointment_title.pack(pady=10)

appointment_frame = Frame(root, bg="lightblue")
appointment_frame.pack()

Label(
    appointment_frame,
    text="Patient Name",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=0, column=0, padx=10, pady=5)

patient_entry = Entry(appointment_frame, font=("Arial", 12))
patient_entry.grid(row=0, column=1)

Label(
    appointment_frame,
    text="Doctor Name",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=1, column=0, padx=10, pady=5)

doctor_entry = Entry(appointment_frame, font=("Arial", 12))
doctor_entry.grid(row=1, column=1)

Label(
    appointment_frame,
    text="Date",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=2, column=0, padx=10, pady=5)

date_entry = Entry(appointment_frame, font=("Arial", 12))
date_entry.grid(row=2, column=1)

Label(
    appointment_frame,
    text="Time",
    font=("Arial", 12),
    bg="lightblue"
).grid(row=3, column=0, padx=10, pady=5)

time_entry = Entry(appointment_frame, font=("Arial", 12))
time_entry.grid(row=3, column=1)

Button(
    appointment_frame,
    text="Book Appointment",
    font=("Arial", 12),
    bg="darkblue",
    fg="white",
    width=18,
    command=book_appointment
).grid(row=4, column=0, pady=10)

Button(
    appointment_frame,
    text="Show Appointments",
    font=("Arial", 12),
    bg="darkgreen",
    fg="white",
    width=18,
    command=show_appointments
).grid(row=4, column=1, pady=10)

# ---------------- APPOINTMENT TABLE ---------------- #

appointment_table_frame = Frame(root)
appointment_table_frame.pack(pady=20)

appointment_table = ttk.Treeview(
    appointment_table_frame,
    columns=("Patient", "Doctor", "Date", "Time"),
    show="headings",
    height=6
)

appointment_table.heading("Patient", text="Patient")
appointment_table.heading("Doctor", text="Doctor")
appointment_table.heading("Date", text="Date")
appointment_table.heading("Time", text="Time")

appointment_table.column("Patient", width=220)
appointment_table.column("Doctor", width=220)
appointment_table.column("Date", width=150)
appointment_table.column("Time", width=150)

appointment_table.pack()

# ---------------- LOAD DATA ---------------- #

show_patients()
show_appointments()

# ---------------- RUN ---------------- #

root.mainloop()

# ---------------- CLOSE DATABASE ---------------- #

conn.close()
