"""Command line menu for the Student Grade Management System.

Run with:  python main.py
"""
import logging
import os

from grade_manager.errors import GradeManagerError
from grade_manager.manager import StudentManager
from grade_manager.report import class_summary, report_card, student_table
from grade_manager.storage import FileStorage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")
LOG_FILE = os.path.join(BASE_DIR, "data", "app.log")

MENU = """
===== Student Grade Management System =====
1. Add student
2. Add / update marks
3. View report card
4. List students (ranked)
5. Search by name
6. Remove a subject
7. Delete student
8. Class summary
0. Exit
"""


def ask(prompt):
    return input(prompt).strip()


def add_student(mgr):
    student = mgr.add_student(ask("Reg. no (e.g. 26BCE10842): "), ask("Name: "))
    print(f"Added {student}")


def add_marks(mgr):
    reg_no = ask("Reg. no: ")
    mgr.get_student(reg_no)  # fail early if the student does not exist
    while True:
        subject = ask("Subject (blank to stop): ")
        if not subject:
            break
        try:
            mgr.set_marks(reg_no, subject, ask("Marks (0-100): "))
            print("Saved.")
        except GradeManagerError as err:
            print("Error:", err)


def view_card(mgr):
    print(report_card(mgr.get_student(ask("Reg. no: "))))


def list_students(mgr):
    print(student_table(mgr.ranked()))


def search(mgr):
    print(student_table(mgr.search_by_name(ask("Name contains: "))))


def remove_subject(mgr):
    mgr.remove_subject(ask("Reg. no: "), ask("Subject to remove: "))
    print("Subject removed.")


def delete_student(mgr):
    student = mgr.get_student(ask("Reg. no: "))
    if ask(f"Really delete {student}? (y/n): ").lower() == "y":
        mgr.delete_student(student.reg_no)
        print("Deleted.")
    else:
        print("Cancelled.")


def show_summary(mgr):
    print(class_summary(mgr))


ACTIONS = {
    "1": add_student, "2": add_marks, "3": view_card, "4": list_students,
    "5": search, "6": remove_subject, "7": delete_student, "8": show_summary,
}


def main():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    manager = StudentManager(FileStorage(DATA_FILE))

    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        if choice == "0":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Please pick a number from the menu.")
            continue
        try:
            action(manager)
        except GradeManagerError as err:
            print("Error:", err)
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled, back to menu.")


if __name__ == "__main__":
    main()
