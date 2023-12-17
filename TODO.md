# 6 classes are added:

## 1. Student()

### Attribute:

- student_ID(str)
- student_first(str)
- student_last(str)

### Method:

- view_request() --> view member_pending_request.csv
- accept_deny_request() --> edit member_pending_request.csv
- change_into_lead() --> edit login.csv
- view_project() --> view project.csv
- modify_project() --> edit project.csv
- create_project() --> add in project.csv

## 2. Lead(Student)

### Attribute:

- info(Student)

### Method:

- request_status() --> view member_pending_request.csv
- send_member_request() --> edit member_pending_request.csv
- send_advisor_request() --> edit advisor_pending_request.csv

## 3. Member(Student)

### Attribute:

- info(Student)

### Method:

- request_status() --> view member_pending_request.csv

## 4. Faculty()

### Attribute:

- faculty_ID(str)
- faculty_first(str)
- faculty_last(str)

### Method:

- view_request() --> view advisor_pending_request.csv
- accept_deny_request() --> edit advisor_pending_request.csv, person.csv  
- view_project() --> view project.csv
- evaluate_project() --> modify project.csv

## 5. Advisor(Faculty)

### Attribute:

- info(Faculty)

### Method:

- view_project() --> view project.csv
- see_project_request()
- advisor_evaluate_project()
- approve_project

## 6. Admin()

### Attribute:

- admin_ID(str)
- admin_first(str)
- admin_last(str)

### Method:

- update_table()
- modify_table()


# 3 Tables are added:

## 1. Project table

### Attributes:
- ProjectID
- Title
- Lead
- Member1
- Member2
- Advisor
- Status

## 2. Advisor_pending_request table

### Attributes:
- ProjectID
- to_be_advisor
- Response
- Response_date

## 3. Member_pending_request table

### Attributes:
- ProjectID
- to_be_member
- Response
- Response_date
