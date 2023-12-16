# import database module 
from database import *
import random
# import copy

db = Database()
# define a function called initializing


def initializing():
    table_names = ['persons', 'login', 'advisor_pending_request', 'member_pending_request', 'project_pending_request', 'project']
    for table_name in table_names:
        csv_reader = ReadCsv(f'{table_name}.csv')
        csv_reader.read_csv()
        table = Table(table_name, csv_reader.data)
        db.insert(table)
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
    table_names = ['persons', 'login', 'advisor_pending_request', 'member_pending_request', 'project_pending_request', 'project']
    for table_name in table_names:
        table = db.search(table_name)
        if table:
            table.readcsv.update_csv(table)
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

        project_id = input("Enter the project ID for which you received an invitation: ")
        response = input("Do you want to accept the project invitation? (yes or no): ")

        for request in request_table.table:
            if request['ProjectID'] == project_id:
                request['Response'] = response
                request_table.readcsv.update_csv(request_table)
                break

        project_found = False
        for project in project_table.table:
            if project['ProjectID'] == project_id:
                project_found = True
                print(f"Project Title: {project['Title']}")
                if response.lower() == 'yes':
                    if project['Member1'] is None or project['Member1'] == '':
                        project['Member1'] = self.student_id
                    else:
                        project['Member2'] = self.student_id
                project_table.readcsv.update_csv(project_table)
                break

        if not project_found:
            print("Project not found.")

    def change_into_lead(self):
        persons_table = db.search('persons')
        persons_table.update({'ID': self.student_id}, {'role': 'lead'})

    def view_project(self):
        project_table = db.search('project')
        choice = input("Which project you want to view (view all(a), by project name(n)): ")
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
        # project_table.update({'ProjectID': project_id}, update_data)

    def create_project(self, project_id, title, lead, member1="", member2="", advisor="",status=""):
        project_table = db.search('project')
        project_table.insert({'projectID': project_id, 'title': title,
                              'lead': lead, 'member1': member1, 'member2': member2, 'advisor': advisor, 'status': status})


class Lead(Student):
    def __init__(self, student_id: str, student_first: str, student_last: str):
        super().__init__(student_id, student_first, student_last)
        self.project_id = random.randrange(000, 999)

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
        request = db.search('member_pending')
        request_data = request.table.filter(lambda x: x['ID'] == self.faculty_id)
        print(request_data)

    def evaluate_project(self):
        pass


class Advisor(Faculty):
    def __init__(self, faculty_id, faculty_first, faculty_last):
        super().__init__(faculty_id, faculty_first, faculty_last)

    def view_project_request(self):
        project_request_table = db.search('project_pending_request')
        for request in project_request_table.table:
            print(f"Project ID: {request['ProjectID']}, Request: {request['to_be_advisor']}, Status: {request['Response']}")

    def accept_deny_project(self):
        project_id = input("Enter the project ID to respond to: ")
        response = input("Accept or Deny the project request? (accept/deny): ")

        project_request_table = db.search('project_pending_request')
        for request in project_request_table.table:
            if request['ProjectID'] == project_id:
                request['Response'] = response
                project_request_table.readcsv.update_csv(project_request_table)
                print(f"Project request for {project_id} has been {response}.")
                break

    def evaluate_project(self):
        project_id = input("Enter the project ID to evaluate: ")
        evaluation = input("Enter your evaluation of the project: ")

        project_table = db.search('project')
        for project in project_table.table:
            if project['ProjectID'] == project_id:
                project['Evaluation'] = evaluation
                project_table.readcsv.update_csv(project_table)
                print(f"Project {project_id} evaluated. Evaluation: {evaluation}")
                break

    def approve_refuse_project(self):
        project_id = input("Enter the project ID to approve or refuse: ")
        decision = input("Approve or Refuse the project? (approve/refuse): ")

        project_table = db.search('project')
        for project in project_table.table:
            if project['ProjectID'] == project_id:
                project['Status'] = 'Approved' if decision.lower() == 'approve' else 'Refused'
                project_table.readcsv.update_csv(project_table)
                print(f"Project {project_id} has been {decision}.")
                break



class Admin:
    def __init__(self, admin_id, admin_first, admin_last):
        self.admin_id = admin_id
        self.admin_first = admin_first
        self.admin_last = admin_last

    def update_table(self):
        table_name = input("Enter the table name that you want to update: ")
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
if val:
    person_info = db.search('persons')
    info = next((i for i in person_info.table if i['ID'] == val[0]), None)
    if info:
        if val[1] == 'admin':
            person = Admin(info['ID'], info['first'], info['last'])
        elif val[1] == 'student':
            person = Student(info['ID'], info['first'], info['last'])
        elif val[1] == 'member':
            person = Member(info['ID'], info['first'], info['last'])
        elif val[1] == 'lead':
            person = Lead(info['ID'], info['first'], info['last'])
        elif val[1] == 'faculty':
            person = Faculty(info['ID'], info['first'], info['last'])
        elif val[1] == 'advisor':
            person = Advisor(info['ID'], info['first'], info['last'])

# once every thing is done, make a call to the exit function
exit()
