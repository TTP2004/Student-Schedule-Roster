import tkinter as tk
from tkinter import messagebox

def displayStudentMenu(username, connection):
    window = tk.Tk()
    window.title(f"Student Menu - {username}")

    def viewClasses():
        cursor = connection.cursor()
        try:
            cursor.callproc('ViewStudentSchedule', (username,))

            classes = []
            for result in cursor.stored_results():
                classes.extend(result.fetchall())

            class_list = "\n".join([f"{c[0]} - {c[1]}" for c in classes])
            messagebox.showinfo("My Classes", class_list if class_list else "No classes found.")
        finally:
            cursor.close()

    def dropClass():
        def submitDrop():
            class_name = entry.get()
            cursor = connection.cursor()
            cursor.callproc('DropRoster', (username, class_name))  # Assume 'DropRoster' is the stored proc for dropping a class
            connection.commit()
            cursor.close()
            messagebox.showinfo("Success", f"Dropped class: {class_name}")
            drop_window.destroy()

        drop_window = tk.Toplevel(window)
        drop_window.title("Drop Class")
        tk.Label(drop_window, text="Enter Class Name:").pack()
        entry = tk.Entry(drop_window)
        entry.pack()
        tk.Button(drop_window, text="Drop", command=submitDrop).pack()

    tk.Button(window, text="View My Classes", command=viewClasses).pack(pady=10)
    tk.Button(window, text="Drop a Class", command=dropClass).pack(pady=10)
    tk.Button(window, text="Exit", command=window.destroy).pack(pady=10)

    window.mainloop()

