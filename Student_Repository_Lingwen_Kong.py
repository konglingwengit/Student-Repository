"""
Author:Lingwen Kong
Date:11/24/2020
Documentation: HW11
"""

from typing import Dict, DefaultDict, List, Tuple
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Lingwen_Kong import file_reader
import os
import sqlite3


class Student:
    """Stores information about a single student with all of the relevant information including:
        cwid
        name
        major
        Container of courses and grades
    """

    def __init__(self, cwid: str, name: str, major: str, required: List, elective: List) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()  # courses[course_name] = grade
        self.stu_course: List = []
        self.stu_grades: List = []
        self.pass_gpa: Dict = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75, 'C+': 2.25, 'C': 2.0}
        self.required: List[str] = required
        self.elective: List[str] = elective

    def store_course_grade(self, course: str, grade: str) -> None:
        """ this student took course and earned grades"""
        if grade in self.pass_gpa:
            self._courses[course] = grade
            self.stu_course.append(course)
            self.stu_grades.append(self.pass_gpa[grade])

    def info(self):
        gpa: float = 0
        if len(self.stu_grades) > 0:
            gpa = round(sum(self.stu_grades) / len(self.stu_grades), 2)
        else:
            gpa = 0.0

        self.required = set(self.required) - set(self._courses)
        if set(self._courses).intersection(set(self.elective)):
            self.elective = []

        return [self._cwid, self._name, sorted(self.stu_course), sorted(self.required), sorted(self.elective), gpa]


class Instructor:
    """ Stores information about a single Instructor with all of the relevant information including:
    cwid
    name
    department
    Container of courses taught and the number of students in each course
    """

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses: DefaultDict[str, int] = defaultdict(
            int)  # courses[course_name] = of students who have taken the course.
        self.stu_course: dict = {}

    def store_course_student(self, course: str):
        # instructor taught course more than one student
        self.courses[course] += 1


class Major:
    """ Stores information about a Major with all of the relevant information including:
        major
        flag for required and elective courses
        courses
        """

    def __init__(self, major: str) -> None:
        self._major: str = major
        self._req_courses: List = []
        self._elec_courses: List = []
        self._courses: Dict[str, Dict] = dict()

    def add_course(self, major: str, flag: str, course: str) -> None:

        if flag == 'R':
            self._req_courses.append(course)
            self._courses[flag] = self._req_courses

        if flag == 'E':
            self._elec_courses.append(course)
            self._courses[flag] = self._elec_courses

    def req_course(self):
        return list(self._req_courses)
        # return self._courses[major]['R']

    def elec_course(self):
        return list(self._elec_courses)

    # return self._courses[major]['E']

    def info(self):
        return [self._major, Major.req_course(self), Major.elec_course(self)]


class Repository:
    """Store all students, instructors for a university and print pretty tables"""

    def __init__(self, path: str, db_path: str) -> None:
        """ init function of class repository"""
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self._majors: Dict[str, Major] = dict()
        self.db_path: str = db_path

        try:
            self._read_major(self._path)
            self._read_instructors(self._path)
            self._read_students(self._path)
            self._read_grades(self._path)

        except (ValueError) as ve:
            print(ve)

        self.major_pretty_table()
        self.student_pretty_table()
        self.instructor_pretty_table()
        self.student_grades_table_db(self.db_path)

    def _read_major(self, path: str) -> None:
        """read each line from file majors.txt and create instance of class Major"""
        try:
            for major, flag, course in file_reader(os.path.join(self._path, 'majors.txt'), 3, "\t", True):
                if major not in self._majors.keys():
                    self._majors[major] = Major(major)
                self._majors[major].add_course(major, flag, course)

        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_students(self, path: str) -> None:
        """read each line from path/students.txt and create instance of class student"""
        try:
            for cwid, name, major in file_reader(os.path.join(self._path, 'students.txt'), 3, "\t", True):
                if major in self._majors.keys():
                    required = self._majors[major].req_course()
                    elective = self._majors[major].elec_course()
                    self._students[cwid] = Student(cwid, name, major, required, elective)

                else:
                    print(f"Student with Name: {name} and CWID: {cwid} has Unknown Major:{major}")

        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_instructors(self, path: str) -> None:
        """read each line from file instructors.txt and create instance of class instructor"""
        try:
            for cwid, name, department in file_reader(os.path.join(self._path, 'instructors.txt'), 3, "\t", True):
                self._instructors[cwid] = Instructor(cwid, name, department)
        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_grades(self, path: str) -> None:
        """ read student_cwid, course, grade, instructor_cwid """
        # tell the student about the course and the grade
        # look up student associated with student_cwid, reach inside and update the dictionary
        try:
            for student_cwid, course, grades, instructor_cwid in file_reader(os.path.join(self._path, 'grades.txt'), 4,
                                                                             "\t", True):
                if student_cwid in self._students.keys():
                    stu: Student = self._students[student_cwid]
                    stu.store_course_grade(course, grades)
                else:
                    print(f"The Student with CWID : {student_cwid} is unknown.")
                if instructor_cwid in self._instructors.keys():
                    inst: Instructor = self._instructors[instructor_cwid]
                    inst.store_course_student(course)
                else:
                    print(f"The Instructor with CWID : {instructor_cwid} is unknown.")
        except (FileNotFoundError, ValueError) as e:
            if FileNotFoundError:
                print(e)

    # tell the instructor that she taught one more student in the course.
    def student_pretty_table(self) -> None:
        """Print pretty table for student data"""
        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Completed Courses', 'Remaining Reuired', 'Remaining Elective', 'GPA'])
        for stu in self._students.values():
            pt.add_row(stu.info())
        print("Student Summary")
        print(pt, "\n")

    def instructor_pretty_table(self) -> None:
        """Print pretty table for instructor data"""
        lst1: List = []
        pt = PrettyTable(field_names=['CWID', 'Name', 'Department', 'Courses', 'Number of Students'])
        for inst in self._instructors.values():
            for k, v in inst.courses.items():
                pt.add_row([inst.cwid, inst.name, inst.dept, k, v])
                lst1.append([inst.cwid, inst.name, inst.dept, k, v])
        print("Instructor Summary")
        print(pt)
        return lst1

    def major_pretty_table(self) -> None:
        """Print pretty table for instructor data"""
        pt = PrettyTable(field_names=['Major', 'Required Courses', 'Elective Courses'])
        for inst in self._majors.values():
            pt.add_row(inst.info())
        print("Majors Summary")
        print(pt)

    def student_grades_table_db(self, db_path) -> None:
        "Print Student Summary for Student Data fetching from a Database File"
        lst2: List = []
        db: sqlite3.Connection = sqlite3.connect(self.db_path)
        pt = PrettyTable(field_names=['Name', 'CWID', 'Course', 'Grade', 'Instructor'])
        for row in db.execute(
                "SELECT s.Name,s.CWID,g.Course,g.Grade,i.Name from students as s JOIN grades as g on g.StudentCWID = s.CWID JOIN instructors as i on g.InstructorCWID = i.CWID order by s.Name ASC"):
            pt.add_row(row)
            lst2.append(row)
        print("Student Grade Summary")
        print(pt)
        return sorted(lst2)


if __name__ == '__main__':
    stevens: Repository = Repository("",
                                     "HW11.db")
