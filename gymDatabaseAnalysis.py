import mysql.connector
from mysql.connector import Error

#Task 1
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

def get_members_in_age_range(start_age, end_age):
    conn = connect_database()
    if conn is not None:
        try:
            start_age = int(start_age)
            end_age = int(end_age)

            cursor = conn.cursor()
            query = "SELECT * FROM Members WHERE age BETWEEN %s AND %s"
            cursor.execute(query, (start_age, end_age))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)
                return results
            else:
                print("Unable to find members within range!")
                return -1
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

get_members_in_age_range(25, 30)