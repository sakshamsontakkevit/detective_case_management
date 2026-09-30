"""StudentManager holds all students and does the add/update/delete work."""
import logging

from .errors import DuplicateStudentError, StudentNotFoundError
from .grading import GradeCalculator
from .models import Student
from .validators import validate_mark, validate_name, validate_reg_no, validate_subject

log = logging.getLogger(__name__)


class StudentManager:
    def __init__(self, storage):
        self.storage = storage
        self.students = storage.load()

    # ---- Create / Read / Update / Delete ----
    def add_student(self, reg_no, name):
        reg_no = validate_reg_no(reg_no)
        name = validate_name(name)
        if reg_no in self.students:
            raise DuplicateStudentError(f"{reg_no} already exists.")
        student = Student(reg_no, name)
        self.students[reg_no] = student
        self._save()
        log.info("Added student %s", reg_no)
        return student

    def get_student(self, reg_no):
        reg_no = validate_reg_no(reg_no)
        if reg_no not in self.students:
            raise StudentNotFoundError(f"No student with reg. no {reg_no}.")
        return self.students[reg_no]

    def set_marks(self, reg_no, subject, mark_text):
        student = self.get_student(reg_no)
        subject = validate_subject(subject)
        mark = validate_mark(mark_text)
        student.set_mark(subject, mark)
        self._save()
        log.info("Set %s = %s for %s", subject, mark, student.reg_no)
        return student

    def remove_subject(self, reg_no, subject):
        student = self.get_student(reg_no)
        removed = student.remove_mark(validate_subject(subject))
        if removed is None:
            raise StudentNotFoundError(f"{student.name} has no subject '{subject}'.")
        self._save()

    def delete_student(self, reg_no):
        student = self.get_student(reg_no)
        del self.students[student.reg_no]
        self._save()
        log.info("Deleted student %s", student.reg_no)

    # ---- Searching and statistics ----
    def search_by_name(self, text):
        text = text.strip().lower()
        return [s for s in self.students.values() if text in s.name.lower()]

    def ranked(self):
        """Students sorted from highest to lowest average."""
        return sorted(self.students.values(), key=lambda s: s.average(), reverse=True)

    def class_average(self):
        if not self.students:
            return 0.0
        return sum(s.average() for s in self.students.values()) / len(self.students)

    def subject_averages(self):
        totals = {}
        for student in self.students.values():
            for subject, mark in student.marks.items():
                totals.setdefault(subject, []).append(mark)
        return {sub: sum(v) / len(v) for sub, v in totals.items()}

    def pass_count(self):
        return sum(1 for s in self.students.values() if GradeCalculator.has_passed(s.marks))

    def _save(self):
        self.storage.save(self.students)
