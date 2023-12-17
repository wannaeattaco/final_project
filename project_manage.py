# import database module 
from database import *
import random

db = Database()


# define a function called initializing


def initializing():
    table_names = ['persons', 'login', 'advisor_pending_request', 'member_pending_request', 'project_pending_request',
                   'project']
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
    table_names = ['persons', 'login', 'advisor_pending_request', 'member_pending_request', 'project_pending_request',
                   'project']
    for table_name in table_names:
        table = db.search(table_name)
        if table:
            table.readcsv.update_csv(table)


# here are things to do in this function:
# write out all the tables that have been modified to the corresponding csv files
# By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:

# https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python
def view_project():
    project_table = db.search('project')
    while True:
        choice = input("Which project you want to view (view all(a), by project name(n)), exit(e): ")
        if choice.lower() == 'a':
            print("Show all projects:")
            for project in project_table.table:
                print(f"Project ID: {project['ProjectID']}")
                print(f"Title: {project['Title']}")
                print(f"Lead: {project['Lead']}")
                print(f"Member no.1: {project['Member1']}")
                print(f"Member no.2: {project['Member2']}")
                print(f"Advisor: {project['Advisor']}")
                print(f"Status: {project['Status']}\n")
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
            print("Invalid choice. Please try again.")


def evaluate_project():
    project_id = input("Enter the project ID to evaluate: ")
    evaluation = input("Enter your evaluation of the project: ")

    project_table = db.search('project')
    project_found = False
    for project in project_table.table:
        if project['ProjectID'] == project_id:
            project_found = True
            if project['Status'] == 'Submitted' or project['Status'] == 'Approved':
                project['Evaluation'] = evaluation
                project['Status'] = 'Scored'
                project_table.readcsv.update_csv(project_table)
                print(f"Project {project_id} evaluated. Evaluation: {evaluation}")
            elif project['Status'] == 'Unfinished':
                print(f"Project {project_id} is not yet submitted for evaluation.")
            elif project['Status'] == 'Scored':
                print(f"Project {project_id} has already been evaluated.")
            else:
                print(f"Project {project_id} has an unrecognized status: {project['Status']}")
            break

    if not project_found:
        print("Project not found.")


class Student:
    def __init__(self, student_id: str, student_first: str, student_last: str):
        self.student_id = student_id
        self.student_first = student_first
        self.student_last = student_last

    def perform_student_action(self):
        while True:
            print("1. View Project Details")
            print("2. Create project")
            print("3. View Member Requests")
            print("4. Accept/Deny member request")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                view_project()
            elif choice == '2':
                self.create_project()
                self.change_into_lead()
            elif choice == '3':
                self.view_request()
            elif choice == '4':
                project_id = input("Enter the project ID for which you received an invitation: ")
                self.accept_deny_request(project_id)
                self.update_project_member(project_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    def view_request(self):
        request_table = db.search('member_pending_request')
        if request_table:
            request_data = [req for req in request_table.table if req['to_be_member'] == self.student_id]

            if request_data:
                for req in request_data:
                    print(req)
            else:
                print("No pending requests found.")
        else:
            print("Member pending request table not found.")

    def accept_deny_request(self, project_id):
        request_table = db.search('member_pending_request')
        project_table = db.search('project')
        persons_table = db.search('persons')
        login_table = db.search('login')

        response = input("Do you want to accept the project invitation? (yes or no): ")

        updated_requests = []
        for request in request_table.table:
            if request['ProjectID'] == project_id:
                request['Response'] = response
                if response.lower() == 'yes':
                    continue
            updated_requests.append(request)
        request_table.table = updated_requests
        request_table.readcsv.update_csv(request_table)

        if response.lower() == 'yes':
            for project in project_table.table:
                if project['ProjectID'] == project_id:
                    if not project['Member1'] or project['Member1'].strip() == '':
                        project['Member1'] = self.student_id
                    elif not project['Member2'] or project['Member2'].strip() == '':
                        project['Member2'] = self.student_id
                    break
            project_table.readcsv.update_csv(project_table)

            for person_in in persons_table.table:
                if person_in['ID'] == self.student_id:
                    person_in['type'] = 'member'
                    break
            persons_table.readcsv.update_csv(persons_table)

            for login_ in login_table.table:
                if login_['ID'] == self.student_id:
                    login_['role'] = 'member'
                    break
            login_table.readcsv.update_csv(login_table)

    def update_project_member(self, project_id):
        project_table = db.search('project')
        project_found = False
        for project in project_table.table:
            if project['ProjectID'] == project_id:
                project_found = True
                if project['Member1'] in (None, '', 'N/A'):
                    project['Member1'] = self.student_id
                elif project['Member2'] in (None, '', 'N/A'):
                    project['Member2'] = self.student_id
                else:
                    print("No available member slots in the project.")
                    return
                project_table.readcsv.update_csv(project_table)
                print(f"Joined project: {project['Title']}")
                break

        if not project_found:
            print("Project not found.")

        if not project_found:
            print("Project not found.")

        if not project_found:
            print("Project not found.")

    def change_into_lead(self):
        persons_table = db.search('persons')
        login_table = db.search('login')
        search_criteria = {'ID': self.student_id}
        update_data_login = {'role': 'lead'}
        update_data_person = {'type': 'lead'}
        persons_table.update(search_criteria, update_data_person)
        login_table.update(search_criteria, update_data_login)

    def modify_project(self, project_id, new_title=""):
        project_table = db.search('project')
        if project_table:
            search_criteria = {'ProjectID': project_id}
            update_data = {}
            if new_title:
                update_data['Title'] = new_title
            if update_data:
                project_table.update(search_criteria, update_data)
            else:
                print("No updates provided.")
        else:
            print("Project table not found.")

    def create_project(self, project_id=None, member1="N/A", member2="N/A", advisor="N/A"):
        title = input("Enter the project title: ")
        lead = input("Enter leader ID:")
        if project_id is None:
            project_id = random.randrange(0, 999)

        project_table = db.search('project')
        new_project = {
            'ProjectID': project_id,
            'Title': title,
            'Lead': lead,
            'Member1': member1,
            'Member2': member2,
            'Advisor': advisor,
            'Status': "Unfinished"
        }
        project_table.insert(new_project)


class Lead(Student):
    def __init__(self, student_id: str, student_first: str, student_last: str, project_id):
        super().__init__(student_id, student_first, student_last)
        self.project_id = project_id

    def perform_lead_action(self):
        while True:
            print("1. View Project Details")
            print("2. Modify Project Details")
            print("3. View Member Requests")
            print("4. Send member invitation")
            print("5. Send advisor request")
            print("6. Summit project")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                view_project()
            elif choice == '2':
                new_title = input("Enter the new project title: ")
                self.modify_project(self.project_id, new_title)
            elif choice == '3':
                self.view_all_request()
            elif choice == '4':
                self.send_member_request()
            elif choice == '5':
                self.send_advisor_request()
            elif choice == '6':
                self.summit_project()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

    def send_member_request(self):
        member_id = input("Enter member ID that you want to send member invitation with: ")
        member_request_table = db.search('member_pending_request')
        if member_request_table:
            member_request_table.insert({'ProjectID': self.project_id, 'to_be_member': member_id})
        else:
            print("Member pending request table not found.")

    def view_all_request(self):
        request_table = db.search('member_pending_request')
        for request in request_table.table:
            print(f"Project ID: {request['ProjectID']}, Member ID: {request['to_be_member']}")

    def send_advisor_request(self):
        advisor_id = input("Enter advisor ID that you want to send advisor request with: ")
        advisor_request_table = db.search('advisor_pending_request')
        if advisor_request_table:
            advisor_request_table.insert({'ProjectID': self.project_id, 'to_be_member': advisor_id})
        else:
            print("Advisor pending request table not found.")

    def summit_project(self):
        project_table = db.search('project')
        project_found = False
        for project in project_table.table:
            if project['ProjectID'] == self.project_id:
                project_found = True
                if project['Status'] == 'Unfinished':
                    project['Status'] = 'Submitted'
                    project_table.readcsv.update_csv(project_table)
                    print(f"Project '{project['Title']}' has been submitted.")
                else:
                    print(f"Project '{project['Title']}' cannot be submitted. Current status: {project['Status']}")
                break

        if not project_found:
            print("Project not found or not associated with the current lead.")


class Member(Student):
    def __init__(self, student_id: str, student_first: str, student_last: str):
        super().__init__(student_id, student_first, student_last)

    def perform_member_action(self):
        while True:
            print("1. View Project Details")
            print("2. Modify Project Details")
            print("3. View Member Requests")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                view_project()
            elif choice == '2':
                project_id = input("Please enter the project ID that you want to modify: ")
                new_title = input("Enter the new project title: ")
                self.modify_project(project_id, new_title)
            elif choice == '3':
                self.view_request()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")


class Faculty:
    def __init__(self, faculty_id, faculty_first, faculty_last):
        self.faculty_id = faculty_id
        self.faculty_first = faculty_first
        self.faculty_last = faculty_last

    def perform_faculty_action(self):
        while True:
            print("1. View Request")
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
                view_project()
            elif choice == '4':
                evaluate_project()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def view_request(self):
        request_table = db.search('advisor_pending_request')
        if request_table:
            request_data = [req for req in request_table.table if req['to_be_member'] == self.faculty_id]

            if request_data:
                for req in request_data:
                    print(req)
            else:
                print("No pending requests found.")
        else:
            print("Member pending request table not found.")

    def accept_deny_advisor_request(self):
        request_table = db.search('advisor_pending_request')
        persons_table = db.search('persons')
        login_table = db.search('login')

        response = input("Do you want to accept the project invitation? (yes or no): ")

        updated_requests = []
        for request in request_table.table:
            request['Response'] = response
            if response.lower() == 'yes':
                continue
        request_table.table = updated_requests
        request_table.readcsv.update_csv(request_table)

        if response.lower() == 'yes':
            for person_in in persons_table.table:
                if person_in['ID'] == self.faculty_id:
                    person_in['type'] = 'advisor'
                    break
            persons_table.readcsv.update_csv(persons_table)
            for login_info in login_table.table:
                if login_info['ID'] == self.faculty_id:
                    login_info['role'] = 'advisor'
                    break
            login_table.readcsv.update_csv(login_table)

    def accept_deny_request(self):
        project_table = db.search('project')

        project_id = input("Enter the project ID for which you received an invitation: ")
        response = input("Do you want to accept the project invitation? (yes or no): ")

        if response.lower() == 'yes':
            for project in project_table.table:
                if project['ProjectID'] == project_id:
                    project['Advisor'] = self.faculty_id
                    break
            project_table.readcsv.update_csv(project_table)


class Advisor(Faculty):
    def __init__(self, faculty_id, faculty_first, faculty_last):
        super().__init__(faculty_id, faculty_first, faculty_last)

    def perform_advisor_action(self):

        while True:
            print("1. View Request")
            print("2. Accept/Deny Request")
            print("3. View project")
            print("4. Evaluate Project")
            print("5. Approve Project")
            print("6. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.view_request()
            elif choice == '2':
                self.accept_deny_request()
            elif choice == '3':
                view_project()
            elif choice == '4':
                evaluate_project()
            elif choice == '5':
                self.approve_project()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def approve_project(self):
        project_table = db.search('project')
        project_id = input("Enter the project ID you want to approve: ")

        project_found = False
        for project in project_table.table:
            if project['ProjectID'] == project_id:
                project_found = True
                project['Status'] = 'Approved'
                break

        if project_found:
            project_table.readcsv.update_csv(project_table)
            print(f"Project ID {project_id} has been approved.")
        else:
            print(f"Project ID {project_id} not found.")


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
            print("You log in as admin")
            person = Admin(info['ID'], info['first'], info['last'])
            person.perform_admin_action()
        elif val[1] == 'student':
            print("You log in as student")
            person = Student(info['ID'], info['first'], info['last'])
            person.perform_student_action()
        elif val[1] == 'member':
            print("You log in as member")
            person = Member(info['ID'], info['first'], info['last'])
            person.perform_member_action()
        elif val[1] == 'lead':
            print("You log in as lead student")
            input_project = input("Enter your project ID: ")
            person = Lead(info['ID'], info['first'], info['last'], input_project)
            person.perform_lead_action()
        elif val[1] == 'faculty':
            print("You log in as faculty")
            person = Faculty(info['ID'], info['first'], info['last'])
            person.perform_faculty_action()
        elif val[1] == 'advisor':
            print("You log in as advisor")
            person = Advisor(info['ID'], info['first'], info['last'])
            person.perform_advisor_action()

# once every thing is done, make a call to the exit function
exit()
