# import database module 
from database import *
# import copy

db = Database()
# define a function called initializing


def initializing():
    # persons table
    advisor_pending = ReadCsv('persons.csv')
    ReadCsv.read_csv(advisor_pending)
    advisor_pending_table = Table('persons', advisor_pending.data)
    db.insert(advisor_pending_table)
    # create a 'persons' table
    # add the 'persons' table into the database
    # for row in person_data:

    # login table
    login_data = ReadCsv('login.csv')
    ReadCsv.read_csv(login_data)
    login_table = Table('login', login_data.data)  # adding dict in list
    db.insert(login_table)

    # advisor pending table
    advisor_pending = ReadCsv('advisor_pending_request.csv')
    ReadCsv.read_csv(advisor_pending)
    advisor_pending_table = Table('advisor_pending', advisor_pending.data)
    db.insert(advisor_pending_table)

    # member pending table
    member_pending = ReadCsv('member_pending_request.csv')
    ReadCsv.read_csv(member_pending)
    member_pending_table = Table('member_pending', member_pending.data)
    db.insert(member_pending_table)

    # project pending table
    project_pending = ReadCsv('project_pending_request.csv')
    ReadCsv.read_csv(project_pending)
    project_pending_table = Table('project_pending', project_pending.data)
    db.insert(project_pending_table)

    # project table
    project = ReadCsv('project_request.csv')
    ReadCsv.read_csv(project)
    project_table = Table('project', project.data)
    db.insert(project_table)
# here are things to do in this function:
    # create an object to read all csv files that will serve as a persistent state for this program

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed

    # add all these tables to the database


# define a function called login
def login():
    username = input("Enter your username here: ")
    password = input("Enter your password here: ")
    login_all = db.search('login')
    for i in login_all.table:
        if username == i['username'] and password == i['password']:
            return [i['ID'], i['role']]
    return None
# here are things to do in this function:
    # add code that performs a login task
    # ask a user for a username and password
    # returns [ID, role] if valid, otherwise returning None


# define a function called exit
def exit():
    ReadCsv.update_csv(db.search("persons"), db.search("persons"))
    ReadCsv.update_csv(db.search("login"), db.search("login"))
# here are things to do in this function:
# write out all the tables that have been modified to the corresponding csv files
# By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
# https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


class Student:
    def __init__(self, student_id: str, student_first: str, student_last: str):
        self.student_id = student_id
        self.student_first = student_first
        self.student_last = student_last

    def view_request(self):
        pass

    def accept_deny_request(self):
        pass

    def change_into_lead(self):
        pass

    def view_project(self):
        pass

    def modify_project(self):
        pass

    def create_project(self):
        pass


class Lead(Student):
    def __init__(self, student_id: str, student_first: str, student_last: str):
        super().__init__(student_id, student_first, student_last)

    def project_status(self):
        pass

    def request_status(self):
        pass

    def send_member_request(self):
        pass

    def send_advisor_request(self):
        pass


class Member(Student):
    def __init__(self, student_id: str, student_first: str, student_last: str):
        super().__init__(student_id, student_first, student_last)

    def project_status(self):
        pass

    def request_status(self):
        pass


class Faculty:
    def __init__(self, faculty_id, faculty_first, faculty_last):
        self.faculty_id = faculty_id
        self.faculty_first = faculty_first
        self.faculty_last = faculty_last

    def view_request(self):
        pass

    def accept_deny_request(self):
        pass

    def view_project(self):
        pass

    def evaluate_project(self):
        pass


class Advisor(Faculty):
    def __init__(self, faculty_id, faculty_first, faculty_last):
        super().__init__(faculty_id, faculty_first, faculty_last)

    def see_project_request(self):
        pass

    def accept_deny_project(self):
        pass

    def evaluate_project(self):
        pass

    def approve_refuse_project(self):
        pass


class Admin:
    def __init__(self, admin_id, admin_first, admin_last):
        self.admin_id = admin_id
        self.admin_first = admin_first
        self.admin_last = admin_last

    def update_table(self):
        pass

    def modify_table(self):
        pass

# make calls to the initializing and login functions defined above


initializing()
val = login()

"based on the return value for login, activate the code that performs activities according to the role defined for that person_id"
person_info = db.search('persons')
info = []
for i in person_info.table:
    if val[0] == i['ID']:
        info.append(i['ID'])
        info.append(i['first'])
        info.append(i['last'])
if val[1] == 'admin':
    person = Admin(info[0], info[1], info[2])
elif val[1] == 'student':
    person = Student(info[0], info[1], info[2])
elif val[1] == 'member':
    person = Member(info[0], info[1], info[2])
elif val[1] == 'lead':
    person = Lead(info[0], info[1], info[2])
elif val[1] == 'faculty':
    person = Faculty(info[0], info[1], info[2])
elif val[1] == 'advisor':
    person = Advisor(info[0], info[1], info[2])

# once every thing is done, make a call to the exit function
exit()
