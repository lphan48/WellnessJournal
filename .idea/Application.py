import sys
import pymysql
import datetime
from prettytable import PrettyTable

def viewExercise(entry_id, cnx, username):
    """
    Handles the CRUD operations for the exercise section
    :param entry_id: the entry to edit
    :param cnx: the current connection to the database
    """
    # read the current status
    c = cnx.cursor()
    c.callproc("getExercise", [str(entry_id)])
    exerciseResult = c.fetchall()
    table = PrettyTable(["Time", "Itensity (1-10)", "Duration", "Exercise Type"])
    for row in exerciseResult:
        table.add_row([row['time'], row['intensity'], row['duration'], row['name']])
    print(table)

    # prompt the user to edit, delete, or go back
    nextAction = input("Press 1 to add a new exercise, 2 to clear it, 3 to pick a different date, or 4 to exit: \n")
    if nextAction == "1":
        data = getExerciseData(entry_id, cnx)
        update_exercise = "INSERT INTO exercise (time, intensity, name, duration, entry_id) " \
                          "VALUES (%s, %s, %s, %s, %s) " \
                          "ON DUPLICATE KEY UPDATE " \
                          "time = VALUES(time), " \
                          "    intensity = VALUES(intensity), name = VALUES(name), duration = VALUES(duration)," \
                          "entry_id = VALUES(entry_id)"
        cursor = cnx.cursor()
        cursor.execute(update_exercise, data)
        cnx.commit()
        viewExercise(entry_id, cnx, username)
    if nextAction == "2":
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM exercise WHERE entry_id = " + str(entry_id))
        cnx.commit()
        viewExercise(entry_id, cnx, username)
    if nextAction == "3":
        displayAllUserEntries(cnx, username)
    if nextAction == "4":
        sys.exit()

def getExerciseData(entry_id, cnx):
    """
    Prompts the user to input valid fields for exercise.
    :param entry_id: entry id
    :param cnx: the current connection
    :return: the data to insert the connection
    """
    cursor = cnx.cursor()
    valid_time = False
    while not valid_time:
        time = input("Enter your exercise time (in the form hh:mm:ss): ")
        hours, minutes, seconds = time.split(":")
        if not time or len(time.split(":")) != 3 or not (hours.isdigit() and minutes.isdigit() and seconds.isdigit()):
            print("Invalid time format. Please enter time in the format hh:mm:ss.")
        else:
            valid_time = True

    valid_intensity = False
    while not valid_intensity:
        intensity = input("Enter your exercise intensity on a scale from 1-10: ")
        if not intensity.isdigit() or int(intensity) < 1 or int(intensity) > 10:
            print("Invalid intensity. Please enter an integer from 1 to 10.")
        else:
            valid_intensity = True

    valid_duration = False
    while not valid_duration:
        duration = input("Enter your exercise duration, as a decimal: ")
        try:
            duration = float(duration)
            valid_duration = True
        except ValueError:
            print("Invalid duration. Please enter a decimal number.")

    exercise_type = input("Enter your exercise name: ")

    cursor.execute("SELECT name FROM Exercise_type")
    row = cursor.fetchone()
    print(row)

    if row['name'] == exercise_type:
        data = (time, int(intensity), exercise_type, duration, entry_id)
    else:
        cursor.execute("INSERT INTO Exercise_type (name) VALUES (%s)", (exercise_type,))
        cnx.commit()
        data = (time, int(intensity), exercise_type, duration, entry_id)

    return data

def viewHydration(entry_id, cnx, username):
    """
    Handles the CRUD operations for the hydration section
    :param entry_id: the entry to edit
    :param cnx: the current connection to the database
    :param username: the name of the user
    """
    # read the current status
    c = cnx.cursor()
    c.callproc("getHydration", [str(entry_id)])
    hydrationResults = c.fetchall()
    table = PrettyTable(["Ounces"])
    for row in hydrationResults:
        table.add_row([row['ounces']])
    print(table)

    # prompt the user to edit, delete, or go back
    nextAction = input("Press 1 to edit this section, 2 to delete it, 3 to pick a different date, or 4 to exit: \n")
    if nextAction == "1":
        data = getHydrationData(entry_id, cnx)
        update_hydration = "INSERT INTO hydration (ounces, entry_id) " \
                           "VALUES (%s, %s) " \
                           "ON DUPLICATE KEY UPDATE " \
                           "ounces = VALUES(ounces), " \
                           "    entry_id = VALUES(entry_id)"
        cursor = cnx.cursor()
        cursor.execute(update_hydration, data)
        cnx.commit()
        viewHydration(entry_id, cnx, username)
    if nextAction == "2":
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM hydration WHERE entry_id = " + str(entry_id))
        cnx.commit()
        viewHydration(entry_id, cnx, username)
    if nextAction == "3":
        displayAllUserEntries(cnx, username)
    if nextAction == "4":
        sys.exit()

def getHydrationData(entry_id, cnx):
    """
    Prompts the user to input the correct hydration data
    :param entry_id: the entry id
    :param cnx: the current connection
    :return: the data to input for hydration
    """
    cursor = cnx.cursor()
    valid_ounces = False
    while not valid_ounces:
        ounce = input("Enter an integer representing the ounces you consumed: \n")
        if ounce.isdigit():
            valid_ounces = True
        else:
            print("Ounces must be an integer.")
    data = (ounce, entry_id)
    return data


def viewNutrition(entry_id, cnx, username):
    """
    Handles the CRUD operations for the nutrition section
    :param entry_id: the entry to edit
    :param cnx: the current connection to the database
    :param username: the username
    :return the data to input for nutrition
    """
    # read the current status
    c = cnx.cursor()
    c.callproc("getNutrition", [str(entry_id)])
    nutritionResult = c.fetchall()
    table = PrettyTable(["Meal Time", "Description", "Meal Name"])
    for row in nutritionResult:
        table.add_row([row['time'], row['description'], row['name']])
    print(table)

    # prompt the user to edit, delete, or go back
    nextAction = input("Press 1 to edit this section, 2 to delete it, 3 to pick a different date, or 4 to exit: \n")
    if nextAction == "1":
        data = getNutritionData(entry_id, cnx)

        update_nutrition = "INSERT INTO nutrition (time, description, name, entry_id) " \
                       "VALUES (%s, %s, %s, %s) " \
                       "ON DUPLICATE KEY UPDATE " \
                       "time = VALUES(time), " \
                       "    time = VALUES(time), " \
                       "    description = VALUES(description), name = VALUES(name), entry_id = VALUES(entry_id)"
        cursor = cnx.cursor()
        cursor.execute(update_nutrition, data)
        cnx.commit()
        viewNutrition(entry_id, cnx, username)
    if nextAction == "2":
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM nutrition WHERE entry_id = " + str(entry_id))
        cnx.commit()
        viewNutrition(entry_id, cnx, username)
    if nextAction == "3":
        displayAllUserEntries(cnx, username)
    if nextAction == "4":
        sys.exit()

def getNutritionData(entry_id, cnx):
    """
    Prompts the user to input correct nutrition data.
    :param entry_id: the entry id
    :param cnx: the current connection
    :return:
    """
    cursor = cnx.cursor()
    valid_time = False
    while not valid_time:
        time = input("Enter your meal time (in the form hh:mm:ss): ")
        hours, minutes, seconds = time.split(":")
        if not time or len(time.split(":")) != 3 or not (hours.isdigit() and minutes.isdigit() and seconds.isdigit()):
            print("Invalid time format. Please enter time in the format hh:mm:ss:")
        else:
            valid_time = True

    description = input("Enter your meal description:\n")

    meal_type = input("Enter your meal name: ")
    cursor.execute("SELECT name FROM Meal")
    row = cursor.fetchone()
    print(row)

    if row['name'] == meal_type:
        data = (time, description, meal_type, entry_id)
    else:
        cursor.execute("INSERT INTO Meal (name) VALUES (%s)", (meal_type,))
        cnx.commit()
        data = (time, description, meal_type, entry_id)

    return data

def viewSleep(entry_id, cnx, username):
    """
    Handles the CRUD operations for the sleep section
    :param entry_id: the entry to edit
    :param cnx: the current connection to the database
    """
    # read the current status
    c = cnx.cursor()
    c.callproc("getSleep", [str(entry_id)])
    sleepResult = c.fetchall()
    table = PrettyTable(["Start Time", "End Time", "Total Hours Slept"])
    for row in sleepResult:
        table.add_row([row['start_time'], row['end_time'], row['total_hours']])
    print(table)

    # prompt the user to edit, delete, or go back
    nextAction = input("Press 1 to edit this section, 2 to delete it, 3 to pick a different date, or 4 to exit: \n")
    if nextAction == "1":
        start = input("Enter your new Start Time:\n")
        end = input("Enter your new End Time:\n")
        total = input("Enter your new Total Hours:\n")
        update_sleep = "INSERT INTO sleep (entry_id, start_time, end_time, total_hours) " \
                       "VALUES (%s, %s, %s, %s) " \
                       "ON DUPLICATE KEY UPDATE " \
                       "start_time = VALUES(start_time), " \
                       "    end_time = VALUES(end_time), " \
                       "    total_hours = VALUES(total_hours), entry_id = VALUES(entry_id)"
        sleep_data = (entry_id, start, end, total)
        cursor = cnx.cursor()
        cursor.execute(update_sleep, sleep_data)
        cnx.commit()
        viewSleep(entry_id, cnx, username)
    if nextAction == "2":
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM sleep WHERE entry_id = " + str(entry_id))
        cnx.commit()
        viewSleep(entry_id, cnx, username)
    if nextAction == "3":
        displayAllUserEntries(cnx, username)
    if nextAction == "4":
        sys.exit()

def viewReflection(entry_id, cnx, username):
    """
    Handles the CRUD operations for the reflection section
    :param entry_id: the entry to edit
    :param cnx: the current connection to the database
    """
    # read the current status
    c = cnx.cursor()
    c.callproc("getReflection", [str(entry_id)])
    reflection_result = c.fetchall()
    table = PrettyTable(["Goal 1", "Goal 2", "Goal 3", "Notes"])
    for row in reflection_result:
        table.add_row([row['goal_one'], row['goal_two'], row['goal_three'], row['notes']])
    print(table)

    # prompt the user to edit, delete, or go back
    nextAction = input("Press 1 to edit this section, 2 to delete it, 3 to pick a different date, or 4 to exit: \n")
    if nextAction == "1":
        goal_one = input("Enter your new Goal 1:\n")
        goal_two = input("Enter your new Goal 2:\n")
        goal_three = input("Enter your new Goal 3:\n")
        notes = input("Enter your new notes:\n")

        update_reflection = "INSERT INTO reflection (goal_one, goal_two, goal_three, notes, entry_id) " \
                            "VALUES (%s, %s, %s, %s, %s) " \
                            "ON DUPLICATE KEY UPDATE " \
                            "goal_one = VALUES(goal_one), " \
                            "    goal_two = VALUES(goal_two), " \
                            "    goal_three = VALUES(goal_three), notes = VALUES(notes), entry_id = VALUES(entry_id)"

        reflection_data = (goal_one, goal_two, goal_three, notes, entry_id)
        cursor = cnx.cursor()
        cursor.execute(update_reflection, reflection_data)
        cnx.commit()
        viewReflection(entry_id, cnx, username)
    if nextAction == "2":
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM reflection WHERE entry_id = " + str(entry_id))
        cnx.commit()
        viewReflection(entry_id, cnx, username)
    if nextAction == "3":
        displayAllUserEntries(cnx, username)
    if nextAction == "4":
        sys.exit()

def displayAllUserEntries(cnx, username):
    c = cnx.cursor()
    c.callproc("getEntryDates", [username])
    entries_result = c.fetchall()

    if entries_result:
        table = PrettyTable(["Current Entries"])
        for row in entries_result:
            table.add_row([row['date']])
        print(table)
    else:
        print("No entries yet!")

    displayOneUserEntry(cnx, username, entries_result)


def displayOneUserEntry(cnx, username, entries_result):
    valid_date = False
    cursor = cnx.cursor()
    while not valid_date:
        date_input = input("Type the date of the entry you'd like to view or create in the format 'YYYY-MM-DD': \n")
        converted_date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()

        try:
            datetime.datetime.strptime(date_input, "%Y-%m-%d")
            date_exists = any(row['date'] == converted_date for row in entries_result)
            valid_date = True

            if not date_exists:
                print("Creating new entry for date " + date_input + "...")
                insert_date = "INSERT INTO Entry (date, day_of_week, user) VALUES (%s, DayofWeek(%s), %s)"
                cursor.execute(insert_date, (converted_date, converted_date, username))

            c = cnx.cursor()
            c.callproc("getEntry", [converted_date, username])
            date_result = c.fetchall()
            table = PrettyTable(["ID", "Date", "Day Index", "User"])
            for row in date_result:
                table.add_row([row['entry_id'], row['date'], row['day_of_week'], row['user']])
            print(table)

            select_entry = "SELECT entry_id FROM Entry WHERE user = %s AND date = %s"
            cursor = cnx.cursor()
            cursor.execute(select_entry, (username, date_input))
            result = cursor.fetchall()
            entry_id = result[0]['entry_id']

        except ValueError:
            print("Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD':\n")

    # ask the user which section they want to crud
    valid_section = False
    while not valid_section:

        section_input = input("Enter journal section you want to view (either 'reflection', "
                                  "'sleep', 'nutrition', 'hydration', or 'exercise' in all lowercase), "
                              "0 to exit the program, or 1 to delete this entry:\n")

        if section_input == 'reflection':
            valid_section = True
            viewReflection(entry_id, cnx, username)

        elif section_input == 'sleep':
            valid_section = True
            viewSleep(entry_id, cnx, username)

        elif section_input == 'nutrition':
            valid_section = True
            viewNutrition(entry_id, cnx, username)

        elif section_input == 'hydration':
            valid_section = True
            viewHydration(entry_id, cnx, username)

        elif section_input == 'exercise':
            valid_section = True
            viewExercise(entry_id, cnx, username)

        elif section_input == "0":
            sys.exit()

        elif section_input == "1":
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM entry WHERE entry_id = " + str(entry_id))
            cnx.commit()
            displayAllUserEntries(cnx, username)

        else:
            print("Invalid journal section. Try again!")


def main():

    # prompt the user for a username and password
    username = input("Enter MySQL username: \n")
    password = input("Enter MySQL password: \n")

    # connect to sharkdb using user input
    try:
        cnx = pymysql.connect(host='localhost', user=username,
                              password=password,
                              db='wellness_journal', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        print("Connection established!\n")
    except pymysql.err.OperationalError:
        print("Connection failed to establish :(\n")
        sys.exit()

    try:
        cursor = cnx.cursor()

        select_usernames = "SELECT username FROM User"
        cursor.execute(select_usernames)
        usernames = [row['username'] for row in cursor.fetchall()]

        # prompt the user to enter a username
        username = input("Enter wellness journal username: \n")

        if username not in usernames:
            first_name = input("Enter your first name: \n")
            last_name = input("Enter your last name: \n")

            # insert new user in the user table
            insert_user = "INSERT INTO User (username, first_name, last_name) VALUES (%s, %s, %s)"
            cursor.execute(insert_user, (username, first_name, last_name))
            print("Create new profile " + username + ", welcome to your new journal, " + first_name + "! :)\n")

        else:
            print("Welcome back, " + username + "!\n")

        # display all current entries for this user
        entry_results = displayAllUserEntries(cnx, username)

        # ask the user which entry they want to crud
        entry_id = displayOneUserEntry(cnx, username, entry_results)



    except pymysql.err.OperationalError as e:
        print('Error:', e.args[0], e.args[1])


if __name__ == "__main__":
    main()