# import database module 
from database import *
import random

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

    def perform_student_action(self):
        while True:
            print("1. View Project Details")
            print("2. Modify Project Details")
            print("3. Create project")
            print("4. View Member Requests")
            print("5. Accept/Deny member request")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_project()
            elif choice == '2':
                project_id = input("Please enter the project ID that you want to verify: ")
                new_title = input("Enter the new project title: ")
                new_lead = input("Enter new leader name:")
                self.modify_project(project_id, new_title, new_lead)
            elif choice == '3':
                title = input("Enter the project title: ")
                lead = input("Enter leader ID:")
                self.create_project(title, lead)
            elif choice == '4':
                self.view_project()
            elif choice == '5':
                self.view_request()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

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
        while True:
            choice = input("Which project you want to view (view all(a), by project name(n)), exit(e): ")
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
            elif choice.lower() == 'n':
                name = input("Enter project name: ")
                project_found = False
                for project in project_table.table:
                    if name.lower() == project['Title'].lower():
                        print(f"Project ID: {project['ProjectID']}")
                        print(f"Title: {project['Title']}")
                        print(f"Lead: {project['Lead']}")
                        print(f"Member no.1: {project['Member1']}")
                        print(f"Member no.2: {project['Member2']}")
                        print(f"Advisor: {project['Advisor']}")
                        print(f"Status: {project['Status']}\n")
                        project_found = True
                        break
                if not project_found:
                    print("Project not found.")
            elif choice.lower() == 'e':
                break
            else:
                print("Which project you want to view (view all(a), by project name(n)), exit(e): ")

    def modify_project(self, project_id, new_title="", new_lead=""):
        project_table = db.search('project')
        project_table.update({'ProjectID': project_id, 'Title': new_title, 'Lead': new_lead})

    def create_project(self, title, lead, project_id=random.randrange(000, 999), member1="", member2="", advisor="", status=""):
        project_table = db.search('project')
        project_table.insert({'ProjectID': project_id, 'Title': title,
                              'Lead': lead, 'Member1': member1, 'Member2': member2, 'Advisor': advisor, 'Status': status})


class Lead(Student):
    def __init__(self, student_id: str, student_first: str, student_last: str, project_id):
        super().__init__(student_id, student_first, student_last)
        self.project_id = project_id

    def perform_lead_action(self):
        while True:
            print("1. View Project Details")
            print("2. Modify Project Details")
            print("3. Create project")
            print("4. View Member Requests")
            print("5. Accept/Deny member request")
            print("6. View member request")
            print("7.Send member invitation")
            print("8. Send advisor request")
            print("9. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_project()
            elif choice == '2':
                project_id = input("Please enter the project ID that you want to verify: ")
                new_title = input("Enter the new project title: ")
                new_lead = input("Enter new leader name:")
                self.modify_project(project_id, new_title, new_lead)
            elif choice == '3':
                title = input("Enter the project title: ")
                lead = input("Enter leader ID:")
                self.create_project(title, lead)
            elif choice == '4':
                self.view_project()
            elif choice == '5':
                self.view_request()
            elif choice == '6':
                self.view_request()
            elif choice == '7':
                member_id = input("Enter member ID that you want to send member invitation with: ")
                self.send_member_request(member_id)
            elif choice == '8':
                advisor_id = input("Enter advisor ID that you want to send advisor request with: ")
                self.send_advisor_request(advisor_id)
            elif choice == '9':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

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

    def perform_member_action(self):
        while True:
            print("1. View Project Details")
            print("2. Modify Project Details")
            print("3. Create project")
            print("4. View Member Requests")
            print("5. Accept/Deny member request")
            print("6. View member request")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_project()
            elif choice == '2':
                project_id = input("Please enter the project ID that you want to verify: ")
                new_title = input("Enter the new project title: ")
                new_lead = input("Enter new leader name:")
                self.modify_project(project_id, new_title, new_lead)
            elif choice == '3':
                title = input("Enter the project title: ")
                lead = input("Enter leader ID:")
                self.create_project(title, lead)
            elif choice == '4':
                self.view_project()
            elif choice == '5':
                self.view_request()
            elif choice == '6':
                self.view_request()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

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

    def perform_faculty_action(self):
        while True:
            print("\n1. View Request")
            print("2. Accept/Deny Request")
            print("3. View Project")
            print("4. Evaluate Project")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_request()
            elif choice == '2':
                self.accept_deny_request()
            elif choice == '3':
                self.view_project()
            elif choice == '4':
                self.evaluate_project()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

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
        project_id = input("Enter the project ID to evaluate: ")
        evaluation = input("Enter your evaluation of the project: ")

        project_table = db.search('project')
        for project in project_table.table:
            if project['ProjectID'] == project_id:
                project['Evaluation'] = evaluation
                project_table.readcsv.update_csv(project_table)
                print(f"Project {project_id} evaluated. Evaluation: {evaluation}")
                break


class Advisor(Faculty):
    def __init__(self, faculty_id, faculty_first, faculty_last):
        super().__init__(faculty_id, faculty_first, faculty_last)

    def perform_advisor_action(self):

        while True:
            print("\n1. View Request")
            print("2. Accept/Deny Request")
            print("3. View Project")
            print("4. Evaluate Project")
            print("5. View Project Request")
            print("6. Accept/Deny Project")
            print("7. Approve/Refuse Project")
            print("8. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.view_request()
            elif choice == '2':
                self.accept_deny_request()
            elif choice == '3':
                self.view_project()
            elif choice == '4':
                self.evaluate_project()
            elif choice == '5':
                self.view_project_request()
            elif choice == '6':
                self.accept_deny_project()
            elif choice == '7':
                self.approve_refuse_project()
            elif choice == '8':
                break
            else:
                print("Invalid choice. Please try again.")

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

    def perform_admin_action(self):
        while True:
            print("\n1. Update Table")
            print("2. Modify Table")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.update_table()
            elif choice == '2':
                self.modify_table()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def update_table(self):
        table_name = input("Enter the table name that you want to update: ")
        table = db.search(table_name)
        if table:
            identifier_key = input("Enter the identifier key: ")
            identifier_value = input("Enter the identifier value: ")
            update_data_str = input("Enter the update data in key:value format, separated by commas: ")

            update_data_pairs = update_data_str.split(',')
            update_dict = {k.strip(): v.strip() for k, v in (pair.split(':') for pair in update_data_pairs)}
            table.update({identifier_key: identifier_value}, update_dict)

    def modify_table(self):
        table_name = input("Enter the table name that you want to modify: ")
        table = db.search(table_name)
        if table:
            action = input("Do you want to add or remove a record? (add/remove): ")
            if action == "add":
                new_record = input("Enter new record data in key:value format, separated by commas: ")

                new_record_pairs = new_record.split(',')
                new_record_dict = {pair.split(':')[0].strip(): pair.split(':')[1].strip() for pair in new_record_pairs}

                table.insert(new_record_dict)
            elif action == "remove":
                identifier_key = input("Enter the identifier key: ")
                identifier_value = input("Enter the identifier value: ")

                table.remove(identifier_key, identifier_value)


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
            person.perform_admin_action()
        elif val[1] == 'student':
            person = Student(info['ID'], info['first'], info['last'])
            person.perform_student_action()
        elif val[1] == 'member':
            person = Member(info['ID'], info['first'], info['last'])
            person.perform_member_action()
        elif val[1] == 'lead':
            input_project = input("Enter your project ID: ")
            person = Lead(info['ID'], info['first'], info['last'], input_project)
            person.perform_lead_action()
        elif val[1] == 'faculty':
            person = Faculty(info['ID'], info['first'], info['last'])
            person.perform_faculty_action()
        elif val[1] == 'advisor':
            person = Advisor(info['ID'], info['first'], info['last'])
            person.perform_advisor_action()

# once every thing is done, make a call to the exit function
exit()
