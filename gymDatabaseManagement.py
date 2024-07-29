import re
import mysql.connector
from mysql.connector import Error

# Task 1
def connect_database():
    db_name = "fitness_center"
    user = "root"
    password = "test"
    host = "localhost"
    conn = ""
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )
        return conn
    except Error as e:
        print(f"Error: {e}")

def add_member(member_name, member_age):
    conn = connect_database()
    if conn is not None:
        try:
            member_name = str(member_name)
            member_age = int(member_age)
            cursor = conn.cursor()
            query = "INSERT INTO Members (name, age) VALUES (%s, %s)"
            cursor.execute(query, (member_name, member_age))
            conn.commit()
            print("Member added successfully!")
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Unable to connect to database!")
        return -1

# Task 2
def search_member_by_id(id_to_search):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = "SELECT * FROM Members WHERE id = %s"
            cursor.execute(query, (id_to_search, ))
            results = cursor.fetchall()
            if results:
                # for row in results:
                #     print(row)
                return results
            else:
                print("Unable to find member!")
                return -1
        finally:
            cursor.close()
            conn.close()

def search_session_by_member_id(member_id):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
            cursor.execute(query, (member_id, ))
            results = cursor.fetchall()
            if results:
                # for row in results:
                #     print(row)
                return results
            else:
                print("Unable to find sessions for that member id!")
                return -1
        finally:
            cursor.close()
            conn.close()
    else:
        print("Unable to connect to database!")
        return -1

def add_session(member_id, session_date, session_time, activity):
    conn = connect_database()
    if conn is not None:
        try:
            member_id = int(member_id)
            session_date = str(session_date)
            session_time = int(session_time)
            activity = str(activity)
            cursor = conn.cursor()
            found_member = search_member_by_id(member_id)
            if found_member == -1:
                print("Member not found!")
                return -1
            # check if there are any sessions for that member
            found_session = search_session_by_member_id(member_id)
            if found_session != -1:#check if date+time combo exist
                if str(found_session[0][2]) == str(session_date) and str(found_session[0][3]) == str(session_time):
                    print("Session already exists for date and time!")
                    return -1
            query = "INSERT INTO WorkoutSessions (member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (member_id, session_date, session_time, activity))
            conn.commit()
            print("Session added successfully!")
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Unable to connect to database!")
        return -1
    
# Task 3
def update_session(session_id, session_date, session_time, session_activity):
    conn = connect_database()
    if conn is not None:
        try:
            session_id = int(session_id)
            session_date = str(session_date)
            session_time = int(session_time)
            session_activity = str(session_activity)
            cursor = conn.cursor()
            updated_session = (session_date, session_time, session_activity, session_id)
            query = "UPDATE WorkoutSessions SET session_date = %s, session_time = %s, activity = %s WHERE session_id = %s"
            cursor.execute(query, updated_session)
            conn.commit()
            print("Session details updated successfully.")
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Unable to connect to database!")
        return -1

def update_member(member_id, new_name, new_age):
    conn = connect_database()
    if conn is not None:
        try:
            new_name = str(new_name)
            new_age = int(new_age)
            cursor = conn.cursor()
            found_member = search_member_by_id(member_id)
            if found_member == -1:
                print("Member not found!")
                return -1
            updated_member = (new_name, new_age, member_id)
            query = "UPDATE Members SET name = %s, age = %s WHERE id = %s"
            cursor.execute(query, updated_member)
            conn.commit()
            print("Session details updated successfully.")
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Unable to connect to database!")
        return -1
    
# Task 4
def delete_session_by_id(id_to_remove):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM WorkoutSessions WHERE session_id = %s"
            cursor.execute(query, (id_to_remove, ))
            conn.commit()
            print("Session deleted successfully")
        finally:
            cursor.close()
            conn.close()

def delete_member_by_id(id_to_remove):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            found_member = search_member_by_id(id_to_remove)
            if found_member == -1:
                print("Member not found!")
                return -1
            
            # check if there are any record of sessions for this member
            query_check = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
            cursor.execute(query_check, (id_to_remove, ))
            sessions = cursor.fetchall()

            if sessions:
                print("Cannot delete member: Member has associated sessions.")
            else:
                query = "DELETE FROM Members WHERE id = %s"
                cursor.execute(query, (id_to_remove, ))
                conn.commit()
                print("Customer removed successfully")
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

def search_member_by_name(member_name, mode):
    conn = connect_database()
    if conn is not None:
        try:
            member_name = str(member_name)
            cursor = conn.cursor()
            if mode == "strict":
                query = "SELECT * FROM Members WHERE name = %s"
            elif mode == "fuzzy":
                query = "SELECT * FROM Members WHERE name LIKE %s"
            cursor.execute(query, (member_name, ))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)
                return results
            else:
                print("Unable to find member!")
                return -1
        finally:
            cursor.close()
            conn.close()
    else:
        print("Unable to connect to database!")
        return -1


add_member("Jimmy", 26)
member = search_member_by_name("Jimmy", "strict")
print("found member by id", search_member_by_id(member[0][0]))
add_session(member[0][0], "2024/7/30", 730, "Weightlifting")
sessions = search_session_by_member_id(member[0][0])
for session in sessions:
    print(session)
delete_session_by_id(sessions[0][0])
delete_member_by_id(member[0][0])
# print(search_member_by_id(13))