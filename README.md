# Final project for 2023's 219114/115 Programming I
* Starting files for part 1
  - database.py
  - project_manage.py
  - persons.csv

### List of files
- Advisor_pending_request.csv → The file for invitation to be advisor of each project
- Database.py → The main file for manage database
- Login.csv → The list of username and password for login
- Member_pending_request.csv → File for add and show the member request for each project
- Persons.csv → list of first, last name role and ID of person
- Project.csv → The list of project
- Project_manage.py → Main file for run and classes

### A description on how to compile and run your project.
The program will start when you login and the program will show the action that can be done which each role for you to choose


Role       | Action                                            | Method                     | Class    |Completion percentage
----------
- Student  | View Project Details                              | view_project()             | Student  | 100%
- Student  | Create project                                    | create_project()           | Student  | 100%
- Student  | View Member Requests                              | view_request()             | Student  | 100%
- Student  | Accept/Deny member request                        | accept_deny_request()      | Student  | 100%
- Student  | Change role from student into lead student        | change_into_lead()         | Student  | 100%
- Student  | Update member name in project                     | update_project_member()    | Student  | 100%
- Lead     | Change project detail                             | modify_project()           | Student  | 100%
- Lead     | View Member Requests                              | view_request()             | Student  | 100%
- Lead     | Send an invitation to student to be a team member | send_member_request()      | Lead     | 100%  
- Lead     | Send an invitation for advisor                    | send_advisor_request()     | Lead     | 100%
- Lead     | Submit finished project                           | submit_project()           | Lead     | 100%
- Lead     | View Project Details                              | view_project()             | Student  | 100%
- Member   | Change project detail                             | modify_project()           | Student  | 100%
- Member   | View Project Details                              | view_project()             | Student  | 100%
- Member   | View Member Requests                              | view_request()             | Student  | 100%
- Faculty  | View advisor invitation                           | view_request()             | Faculty  | 100%  
- Faculty  | Accept/Deny advisor request                       | accept_deny_request()      | Faculty  | 100%
- Faculty  | View Project Details                              | view_project()             | Faculty  | 100%  
- Faculty  | Evaluate project as faculty                       | faculty_evaluate_project() | Faculty  | 100%
- Advisor  | Accept/Deny advisor request                       | accept_deny_request()      | Faculty  | 100%
- Advisor  | View advisor invitation                           | view_request()             | Faculty  | 100%
- Advisor  | View Project Details                              | view_project()             | Faculty  | 100%
- Advisor  | Evaluate project as advisor                       | advisor_evaluate_project() | Faculty  | 100%
- Advisor  | Approve project                                   | approve_project()          | Advisor  | 100%
- Admin    | Update Table                                      | update_table()             | Admin    | 100%
- Admin    | Modify Table                                      | modify_table()             | Admin    | 100%

### Missing feature

Evaluation of project not complete to use bcause the function is not in the same function

