import tkinter as tk
from tkinter import simpledialog, messagebox

def display_manager_menu(username, connection):
    window = tk.Tk()
    window.title(f"Manager Menu - {username}")

    def view_student_schedule_ui():
        student = simpledialog.askstring("Student Username", "Enter Student Username:")
        if not student:
            return
        cursor = connection.cursor()
        cursor.callproc("ViewStudentSchedule", (student,))
        student_schedule = []
        for result in cursor.stored_results():
            student_schedule.extend(result.fetchall())
        cursor.close()
        messagebox.showinfo("Student Schedule", "\n".join([f"{s[0]} - {s[1]}" for s in student_schedule]) if student_schedule else "No classes found.")

    def view_class_roster_ui():
        class_name = simpledialog.askstring("Class Name", "Enter Class Name:")
        if not class_name:
            return
        cursor = connection.cursor()
        cursor.callproc("ViewClassRoster", (class_name,))
        class_roster = []
        for result in cursor.stored_results():
            class_roster.extend(result.fetchall())
        cursor.close()
        messagebox.showinfo("Class Roster", "\n".join([str(c[0]) for c in class_roster]) if class_roster else "No students found.")

    def add_student_to_roster_ui():
        student = simpledialog.askstring("Student Username", "Enter Student Username:")
        class_name = simpledialog.askstring("Class Name", "Enter Class Name:")
        if not student or not class_name:
            return
        cursor = connection.cursor()
        cursor.callproc("AddRoster", (student, class_name))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Success", f"Added {student} to {class_name}.")

    def drop_student_from_roster_ui():
        student = simpledialog.askstring("Student Username", "Enter Student Username:")
        class_name = simpledialog.askstring("Class Name", "Enter Class Name:")
        if not student or not class_name:
            return
        cursor = connection.cursor()
        cursor.callproc("DropRoster", (student, class_name))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Success", f"Dropped {student} from {class_name}.")

    def add_new_student_ui():
        username = simpledialog.askstring("New Username", "Enter New Student Username:")
        password = simpledialog.askstring("New Password", "Enter New Student Password:")
        fname = simpledialog.askstring("First Name", "Enter First Name:")
        lname = simpledialog.askstring("Last Name", "Enter Last Name:")
        major_id = simpledialog.askinteger("Major ID", "Enter Major ID:")
        role_id = "stu"  # Assuming role_id stu corresponds to student
        if not username or not password or not fname or not lname or major_id is None:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        cursor = connection.cursor()
        cursor.callproc("AddStudent", (username, password, fname, lname, role_id, major_id))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Success", f"Added new student: {username}.")

    # UI Buttons
    tk.Button(window, text="View Student Schedule", command=view_student_schedule_ui).pack(pady=10)
    tk.Button(window, text="View Class Roster", command=view_class_roster_ui).pack(pady=10)
    tk.Button(window, text="Add Student to Roster", command=add_student_to_roster_ui).pack(pady=10)
    tk.Button(window, text="Drop Student from Roster", command=drop_student_from_roster_ui).pack(pady=10)
    tk.Button(window, text="Add New Student", command=add_new_student_ui).pack(pady=10)
    tk.Button(window, text="Exit", command=window.destroy).pack(pady=10)

    window.mainloop()