import os
import tempfile
import unittest

from grade_manager.errors import (DuplicateStudentError, StudentNotFoundError,
                                  ValidationError)
from grade_manager.manager import StudentManager
from grade_manager.storage import FileStorage


class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "students.json")
        self.mgr = StudentManager(FileStorage(self.path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_duplicate(self):
        self.mgr.add_student("26bce10842", "saksham sontakke")
        self.assertEqual(self.mgr.get_student("26BCE10842").name, "Saksham Sontakke")
        with self.assertRaises(DuplicateStudentError):
            self.mgr.add_student("26BCE10842", "Someone")

    def test_bad_input(self):
        with self.assertRaises(ValidationError):
            self.mgr.add_student("123", "Abc")
        self.mgr.add_student("26BCE10842", "Saksham")
        with self.assertRaises(ValidationError):
            self.mgr.set_marks("26BCE10842", "Python", "150")

    def test_missing_student(self):
        with self.assertRaises(StudentNotFoundError):
            self.mgr.get_student("26BCE99999")

    def test_ranking_and_average(self):
        self.mgr.add_student("26BCE10001", "Asha")
        self.mgr.add_student("26BCE10002", "Ravi")
        self.mgr.set_marks("26BCE10001", "Python", "60")
        self.mgr.set_marks("26BCE10002", "Python", "90")
        self.assertEqual(self.mgr.ranked()[0].name, "Ravi")
        self.assertEqual(self.mgr.class_average(), 75.0)

    def test_data_survives_reload(self):
        self.mgr.add_student("26BCE10842", "Saksham")
        self.mgr.set_marks("26BCE10842", "Python", "88")
        again = StudentManager(FileStorage(self.path))
        self.assertEqual(again.get_student("26BCE10842").marks["Python"], 88.0)

    def test_delete(self):
        self.mgr.add_student("26BCE10842", "Saksham")
        self.mgr.delete_student("26BCE10842")
        self.assertEqual(len(self.mgr.students), 0)


if __name__ == "__main__":
    unittest.main()
