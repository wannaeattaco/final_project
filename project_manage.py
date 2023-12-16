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
    project = ReadCsv('project.csv')
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
    for login_info in login_all.table:
        if username == login_info['username'] and password == login_info['password']:
            return [login_info['ID'], login_info['role']]
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
        request = db.search('member_pending')
        request_data = request.table.filter(lambda x: x['ID'] == self.student_id)
        print(request_data)

    def accept_deny_request(self):
        request_table = db.search('member_pending')
        project_table = db.search('project')
        project_id = request_table['ID']
        response = input("Do you want to accept project invitation? (yes or no):")
        request_table.update({'ProjectID': project_id}, {'Response': response})
        if project_table['Member1'] is None:
            project_table.update({'ProjectID': project_id}, {'Member1': self.student_id})
        else:
            project_table.update({'ProjectID': project_id}, {'Member2': self.student_id})
        # print(f"{} invitation accepted")

    def change_into_lead(self):
        persons_table = db.search('persons')
        persons_table.update({'ID': self.student_id}, {'role': 'lead'})

    def view_project(self):
        project_table = db.search('project')
        choice = input("Which project you want to view (view all(a), by name(n)): ")
        if choice.lower() == 'a':
            for project in project_table:
                project(f"Project number {project}")
                print(f"Project ID: {project['ProjectID']}")
                print(f"Title: {project['Title']}")
                print(f"Lead: {project['Lead']}")
                print(f"Member no.1 {project['Member1']}")
                print(f"Member no.2 {project['Member2']}")
                print(f"Advisor: {project['Advisor']}")
                print(f"Status: {project['Status']}")
        if choice.lower() == 'n':
            name = input("Enter project name: ")
            for project in project_table:  # change to while
                if name == project['Title']:
                    print(f"Project ID: {project['ProjectID']}")
                    print(f"Title: {project['Title']}")
                    print(f"Lead: {project['Lead']}")
                    print(f"Member no.1 {project['Member1']}")
                    print(f"Member no.2 {project['Member2']}")
                    print(f"Advisor: {project['Advisor']}")
                    print(f"Status: {project['Status']}")

    def modify_project(self):
        project_table = db.search('project')
        project_id = input("Please enter the project ID that you want to verify: ")
        project_table.update({'ProjectID': project_id}, update_data)

    def create_project(self, project_id, title, lead, member1="", member2="", advisor="",status=""):
        project_table = db.search('project')
        project_table.insert({'projectID': project_id, 'title': title,
                              'lead': lead, 'member1': member1, 'member2': member2, 'advisor': advisor, 'status': status})


class Lead(Student):
    def __init__(self, student_id: str, student_first: str, student_last: str, project_id=""):
        super().__init__(student_id, student_first, student_last)
        self.project_id = project_id

    def project_status(self):
        pass

    def view_request(self):
        request = db.search('member_pending')
        request_data = request.table.filter(lambda x: x['ID'] == self.student_id)
        print(request_data)

    def send_member_request(self, member_id):
        member_request_table = db.search('member_pending')
        member_request_table.insert({'ProjectID': self.project_id, 'to_be_member': member_id})

    def send_advisor_request(self, advisor_id):
        member_request_table = db.search('member_pending')
        member_request_table.insert({'ProjectID': self.project_id, 'to_be_member': advisor_id})


class Member(Student):
    def __init__(self, student_id: str, student_first: str, student_last: str):
        super().__init__(student_id, student_first, student_last)

    def project_status(self):
        pass

    def request_status(self):
        request_table = db.search('member_pending')
        for request in request_table.table:
            if request['to_be_member'] == self.student_id:
                print(request)


class Faculty:
    def __init__(self, faculty_id, faculty_first, faculty_last):
        self.faculty_id = faculty_id
        self.faculty_first = faculty_first
        self.faculty_last = faculty_last

    def view_request(self):
        request = db.search('advisor_pending')
        request_data = request.table.filter(lambda x: x['ID'] == self.faculty_id)
        print(request_data)

    def accept_deny_request(self):
        request_table = db.search('member_pending')
        project_table = db.search('project')
        project_id = request_table['ID']
        response = input("Do you want to accept project invitation? (yes or no):")
        request_table.update({'ProjectID': project_id}, {'Response': response})
        project_table.update({'ProjectID': project_id}, {'Member1': self.faculty_id})

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
        table = db.search(table_name)
        if table:
            for data in update_data:
                table.update(data['identifier_key'], data['identifier_value'], data['update'])

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
