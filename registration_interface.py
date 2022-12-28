def get_choice(choice_list):
    '''
    This function takes a list of choices as a parameter and prompts the user to enter a choice
    until the user enters a choice that is inside the list. Once the user enters a valid choice,
    the function returns that choice. 
    
    Input: choice_list (A list containing the options as elements)
    Output: choice (The final choice that is in the list)
    '''
    while True:
        choice = input("Enter choice> ")
        if choice in choice_list:
            return choice
            break 
        print("Invalid choice!")    
        
        
def courses_by_subject():
    '''
    This function prompts the user to select a subject of interest among the list of available subjects using the get_choice function 
    and displays the classid, subject, course number, section, meeting time, instructor's first and last names 
    for all the courses offered in the spring for that particular subject. 
    
    Input: None
    Output: None
    '''
    
    # create engine, connection
    engine = sa.create_engine("sqlite+pysqlite:///school.db")
    connection = engine.connect()

    # execute a query on one of the tables
    result_proxy = connection.execute("""
    SELECT DISTINCT coursesubject
    FROM classes
    WHERE classterm = "SPRING"
    ORDER BY coursesubject ASC
    ;
    """)

    result_list = result_proxy.fetchall()
    
    # get the list of subjects
    subject_list = [element[0] for element in result_list]
    print("\nAvailable subjects:", subject_list)
    
    print("\nSelect your subject of interest: ")
    
    # call get_choice function
    subject = get_choice(subject_list)
    
    # perform a multitable SQL query
    result_proxy = connection.execute("""
    SELECT c.classid, c.coursesubject, c.coursenum, c.classsection, c.classmeeting, i.instructorfirst, i.instructorlast
    FROM classes AS c INNER JOIN instructor_class AS ic USING (classid)
                      INNER JOIN instructors AS i USING (instructorid)
    WHERE c.classterm = "SPRING" AND c.coursesubject = '""" + subject + """'
    ORDER BY c.coursenum ASC
    ;
    """)
    
    result_list = result_proxy.fetchall()  
    for result in result_list:
        print (result)
       
        
def courses_by_time():
    '''
    This function prompts the user to select a time of interest among the list of available time slots using the get_choice function 
    and displays the classid, subject, course number, section, meeting time, instructor's first and last names 
    for all the courses offered in the spring for that particular time slot. 
    
    Input: None
    Output: None
    '''
    
    # create engine, connection
    engine = sa.create_engine("sqlite+pysqlite:///school.db")
    connection = engine.connect()

    # execute a query on one of the tables
    result_proxy = connection.execute("""
    SELECT DISTINCT classmeeting
    FROM classes
    WHERE classterm = "SPRING" AND classmeeting IS NOT NULL
    ORDER BY classmeeting ASC
    ;
    """)

    result_list = result_proxy.fetchall()
    
    # get the list of time slots
    time_list = [element[0] for element in result_list]
    print("\nAvailable times:", time_list)
    
    print("\nSelect your time of interest: ")
    
    # call get_choice function
    time = get_choice(time_list)
    
    # perform a multitable SQL query
    result_proxy = connection.execute("""
    SELECT c.classid, c.coursesubject, c.coursenum, c.classsection, c.classmeeting, i.instructorfirst, i.instructorlast
    FROM classes AS c INNER JOIN instructor_class AS ic USING (classid)
                      INNER JOIN instructors AS i USING (instructorid)
    WHERE c.classterm = "SPRING" AND c.classmeeting = '""" + time + """'
    ORDER BY c.coursesubject ASC, c.coursenum ASC
    ;
    """)
    
    result_list = result_proxy.fetchall()
    for result in result_list:
        print(result)
        
        
def get_registered_courses():
    '''
    This function prompts the user to enter their studentid using the get_choice function 
    and displays the classid, subject, course number, section, meeting time, instructor's first and last names 
    for all the courses that the student is registered in for the spring semester.
    
    Input: None
    Output: None
    '''
    # create engine, connection
    engine = sa.create_engine("sqlite+pysqlite:///school.db")
    connection = engine.connect()

    # execute a query on one of the tables
    result_proxy = connection.execute("""
    SELECT studentid
    FROM students
    ORDER BY studentid ASC
    ;
    """)

    result_list = result_proxy.fetchall()
    
    # get a list of studentids
    studentid_list = [str(element[0]) for element in result_list]
    
    print("\nEnter your studentid: ")
    
    # call get_choice function
    user_studentid = get_choice(studentid_list)

    # perform a multitable SQL query
    result_proxy = connection.execute("""
    SELECT c.classid, c.coursesubject, c.coursenum, c.classsection, c.classmeeting, i.instructorfirst, i.instructorlast
    FROM student_class AS sc INNER JOIN classes AS c USING (classid)
                             INNER JOIN instructor_class AS ic USING (classid)
                             INNER JOIN instructors AS i USING (instructorid)
    WHERE c.classterm = "SPRING" AND sc.status = "**Registered**" AND sc.studentid = """ + user_studentid + """
    ;
    """)
    
    result_list = result_proxy.fetchall()
    for result in result_list:
        print(result)
        
        
def total_credit_hours():
    '''
    This function prompts the user to enter their studentid using the get_choice function
    and displays the total credit hours that the student is enrolled in for the spring semester.
    
    Input: None
    Output: None
    '''
    # create engine, connection
    engine = sa.create_engine("sqlite+pysqlite:///school.db")
    connection = engine.connect()

    # execute a query on one of the tables
    result_proxy = connection.execute("""
    SELECT studentid
    FROM students
    ORDER BY studentid ASC
    ;
    """)

    result_list = result_proxy.fetchall()
    
    # get a list of studentids
    studentid_list = [str(element[0]) for element in result_list]
    
    print("\nEnter your studentid: ")
    
    # call get_choice function
    user_studentid = get_choice(studentid_list)

    # perform a multitable SQL query
    result_proxy = connection.execute("""
    SELECT SUM(co.coursehours) AS total_credit_hrs
    FROM student_class AS sc INNER JOIN classes AS c USING (classid)
                             INNER JOIN courses AS co ON (c.coursesubject = co.coursesubject AND c.coursenum = co.coursenum)
    WHERE c.classterm = "SPRING" AND sc.status = "**Registered**" AND sc.studentid = """ + user_studentid + """
    ;
    """)
    
    result_list = result_proxy.fetchall()
    for result in result_list:
        print(result[0])
        
        
# import sqlalchemy
import sqlalchemy as sa

def main():
    '''
    This is a main function that gives a menu of options and repeatedly asks the user to select an option.
    It shows the outcome that corresponds to the user's option and continues to ask the user
    to select options until the quit option is selected. 
    '''
    
    print("Welcome to the registration database!")
    
    while True:
        
        # show the options
        print("""\n1. Show all courses by subject
2. Show all courses by time slot
3. Show all your registered courses
4. Show total credit hours 
5. Quit program""")
        print("======================================")
        print("Please select option 1-4: ")
        
        # call get_choice function
        option = get_choice(["1","2","3","4","5"])
        
        # call each function according to the selected option
        if option == "1":
            courses_by_subject()
        elif option == "2":
            courses_by_time()
        elif option == "3":
            get_registered_courses()
        elif option == "4":
            total_credit_hours()
        elif option == "5":
            print("Shutting down...")
            # close up connections
            try:
                connection.close()
                del engine
            except:
                pass
            # break out of a loop 
            break
            
main()