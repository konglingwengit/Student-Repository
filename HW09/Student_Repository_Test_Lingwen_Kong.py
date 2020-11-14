import unittest
from Student_Repository_Lingwen_Kong import Repository
import os

class TestRepository(unittest.TestCase):
    def test_repository(self):
        # pass directory path with all files
        test_obj = Repository(os.getcwd()+'/hw9/')
        # validation
        self.assertEqual(len(test_obj.instructors), 6)
        self.assertEqual(len(test_obj.students), 10)
        self.assertEqual(test_obj.instructors.get('98765').name, 'Einstein, A')
        self.assertEqual(test_obj.instructors.get('98765').dept, 'SFEN')
        self.assertEqual(test_obj.instructors.get('98765').course, {'SSW 567': 4, 'SSW 540': 3})
        self.assertEqual(test_obj.students.get('11788').name, 'Fuller, E')
        self.assertEqual(test_obj.students.get('11788').major, 'SYEN')
        self.assertEqual(test_obj.students.get('11788').course['SSW 540'], 'A')
        self.assertEqual(test_obj.students.get('11788').course['SSW 541'], '')


if __name__ == '__main__':
    unittest.main()
