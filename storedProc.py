#Login Function
def get_all_users(connection):
    try:
        cursor = connection.cursor()
        cursor.callproc("GetAllUsers")
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        cursor.close()
        return results
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []



# Student Functions
# View a student's own class schedule (ClassCode + ClassName)
def view_student_schedule(connection, username):
    try:
        cursor = connection.cursor()
        cursor.callproc("ViewStudentSchedule", (username,))
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        cursor.close()
        return results
    except Exception as e:
        return f"Error viewing student schedule: {e}"

# Drop a class for themselves (Student dropping their own class)
def drop_student_own_class(connection, username, class_code):
    try:
        cursor = connection.cursor()
        cursor.callproc("DropStudentClass", (username, class_code))
        connection.commit()
        cursor.close()
        return "Class dropped successfully."
    except Exception as e:
        return f"Error dropping your class: {e}"


#Manager Functions
# View a class roster (Show full names)
def view_class_roster(connection, class_code):
    try:
        cursor = connection.cursor()
        cursor.callproc("ViewClassRoster", (class_code,))
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        cursor.close()
        return results
    except Exception as e:
        return f"Error viewing class roster: {e}"

# Add a student to a class roster
def add_student_to_roster(connection, username, class_code):
    try:
        cursor = connection.cursor()
        cursor.callproc("AddRoster", (username, class_code))
        connection.commit()
        cursor.close()
        return "Student added to class successfully."
    except Exception as e:
        return f"Error adding student to class: {e}"

# Drop a student from a class roster (Manager dropping any student)
def drop_student_from_roster(connection, username, class_code):
    try:
        cursor = connection.cursor()
        cursor.callproc("DropRoster", (username, class_code))
        connection.commit()
        cursor.close()
        return "Student dropped from class successfully."
    except Exception as e:
        return f"Error dropping student from class: {e}"

# Add a brand-new student (Username, Password, First Name, Last Name, RoleID, MajorID)
def add_student(connection, username, password, fname, lname, role_id, major_id):
    try:
        cursor = connection.cursor()
        cursor.callproc("AddStudent", (username, password, fname, lname, role_id, major_id))
        connection.commit()
        cursor.close()
        return "Student added successfully."
    except Exception as e:
        return f"Error adding student: {e}"