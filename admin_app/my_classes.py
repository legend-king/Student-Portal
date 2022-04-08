class Student:
    def __init__(self, name, id, email, dept='', year='', section='',semseter=''):
        self.name=name
        self.id=id
        self.email=email
        self.dept=dept
        self.year=year
        self.semester=semseter
        self.section=section

class Subject:
    def __init__(self, sub_code, sub_name):
        self.sub_name=sub_name
        self.sub_code=sub_code

class Subject_Detail:
    def __init__(self, value, key):
        self.key=key
        self.value=value

class Attendance:
    def __init__(self, dept, sem, year, sub_code, date, staff_code, section):
        self.dept=dept
        self.sem=sem
        self.year=year
        self.sub_code=sub_code
        self.date=date
        self.staff_code=staff_code
        self.section=section