from datetime import datetime
import random


class Course:

    courseCodeSeed = 100

    def __init__(self, name, corp, credit, hpw):
        self.department = "Computer Science"
        self.courseinitials = "CP"
        self.course_name = name
        self.corp = corp
        self.credit = credit
        self.hpw = hpw
        
        self.code = self.generateCourceCode()
        self.hasLab = True

    def show_info(self):
        print(f"Course Name: {self.course_name}")
        print(f"Course Coordinator : {self.corp}")
        print(f"Credit: {self.credit}")
        print(f"Code: {self.code}")
        print(f"Hours per week: {self.hpw}")

    def get_info(self, infoname):

        if infoname == "name":
            return self.name
        elif infoname == "corp":
            return self.professor
        elif infoname == "credit":
            return self.credit
        elif infoname == "code":
            return self.code
        elif infoname == "hpw":
            return self.hoursperweek
        else:
            return "Invalid infoname"

    def generateCourceCode(self):
        code = f"{datetime.now().year}{self.courseinitials}{Course.courseCodeSeed}"
        Course.courseCodeSeed += 1
        return code


class Lecture(Course):
    def __init__(
        self,
        name,
        corp,
        credit,
        professor,
        hpw,
    ):
        super().__init__(name, corp, credit, hpw)
        self.professor = professor

    def show_info(self):
        super().show_info()
        print(f"Professor: {self.professor}")

    def get_info(self, infoname):
        if infoname == "professor":
            return self.professor
        else:
            return super().get_info(infoname)
