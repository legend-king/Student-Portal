from django.db import models

# Create your models here.
class Attendance:
    def __init__(self, staff_code, key, dept, section, year, sem, sub_code):
        self.staff_code=staff_code
        self.key=key
        self.dept=dept
        self.section=section
        self.year=year
        self.sem=sem
        self.sub_code=sub_code


class AttendanceDetail:
    def __init__(self, date, hour, dh):
        self.date=date
        self.hour=hour
        self.dh=dh

class AttendanceDH:
    def __init__(self, regno, present):
        self.regno=regno
        self.present=present