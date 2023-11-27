# 6 classes are added:

## 1. Student()

### Attribute:

- student_ID(str)
- student_first(str)
- student_last(str)

### Method:

- view_request()
- accept_deny_request()
- change_into_lead()
- view_project()
- modify_project()

## 2. Lead(Student)

### Attribute:

- info(Student)

### Method:

- project_status()
- request_status()
- create_project()
- send_member_request()
- send_advisor_request()

## 3. Member(Student)

### Attribute:

- info(Student)

### Method:

- project_status()
- request_status()

## 4. Faculty()

### Attribute:

- faculty_ID(str)
- faculty_first(str)
- faculty_last(str)

### Method:

- view_request()
- accept_deny_request()
- view_project()
- evaluate_project()

## 5. Advisor(Faculty)

### Attribute:

- info(Faculty)

### Method:

- view_project()
- see_project_request()
- accept_deny_project()
- evaluate_project()
- approve_refuse_project()

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
