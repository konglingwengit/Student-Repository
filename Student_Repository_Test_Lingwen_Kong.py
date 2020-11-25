from typing import Dict, List
import unittest

from Student_Repository_Lingwen_Kong import Repository


class Test(unittest.TestCase):
    """Helps to test all the functions"""

    def test_data_for_Student(self):
        """This function is used to test data_for_student function's output"""
        self.stevens: Repository = Repository("",
                                              "HW11.db")

        calculated: List = [['10103', 'Jobs, S', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38],
                            ['10115', 'Bezos, J', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 4.0],
                            ['10183', 'Musk, E', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.0],
                            ['11714', 'Gates, B', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5]]

        calculated2: List = [student.info() for cwid, student in self.stevens._students.items()]
        self.assertEqual(calculated, calculated2)

    def test_data_for_Instructor(self):
        """This function is used to test data_for_instructor function's output"""
        stevens: Repository = Repository("",
                                         "HW11.db")
        calculated: List = [['98764', 'Cohen, R', 'SFEN', 'CS 546', 1],
                            ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                            ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1],
                            ['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                            ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                            ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]

        self.assertEqual(stevens.instructor_pretty_table(), calculated)

    def test_data_for_Major(self):
        """This function is used to test data_for_major function's output"""
        self.stevens: Repository = Repository("",
                                              "HW11.db")

        calculated: List = [['SFEN', ['SSW 540', 'SSW 810', 'SSW 555'], ['CS 501', 'CS 546']],
                            ['CS', ['CS 570', 'CS 546'], ['SSW 810', 'SSW 565']]]

        calculated2: List = [course.info() for major, course in self.stevens._majors.items()]
        self.assertEqual(calculated, calculated2)

    def test_data_for_student_grades_summary(self):
        """This function is used to test data_for_major function's output"""
        stevens: Repository = Repository("",
                                         "HW11.db")

        calculated: List = [('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                            ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                            ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                            ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                            ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                            ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                            ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                            ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                            ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')]

        self.assertEqual(
            stevens.student_grades_table_db("HW11.db"),
            calculated)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
