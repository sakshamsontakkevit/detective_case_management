# Student Grade Management System

**Author:** Saksham Sontakke (Reg. No: 26BCE10842), VIT Bhopal
**Course:** Python Essentials

## Overview
A command-line application to manage student marks. It calculates letter grades,
GPA, pass/fail results and class rankings. Data is saved in a JSON file so it is
still there the next time you run the program. No database is used.

## Features
- Add, search and delete students (validated registration numbers)
- Add or update marks for any subject (0-100)
- Report card with letter grade, average, GPA and result
- Ranked list of students and a class summary with subject averages
- Input validation, custom exceptions and a log file (`data/app.log`)
- Unit tests using Python's built-in `unittest`

## Technologies Used
Python 3.8+ (standard library only: `json`, `re`, `logging`, `unittest`).
Concepts used: classes and objects, class methods, custom exceptions, dictionaries,
file handling, modules and packages.

## Project Structure
```
student-grade-manager/
├── main.py                 # menu and program start
├── grade_manager/
│   ├── models.py           # Student class
│   ├── grading.py          # GradeCalculator class
│   ├── manager.py          # StudentManager class (add/update/delete/stats)
│   ├── storage.py          # FileStorage class (JSON file)
│   ├── validators.py       # input checks
│   ├── errors.py           # custom exceptions
│   └── report.py           # text output
├── tests/                  # unit tests
├── data/                   # students.json and app.log are created here
├── statement.md
└── requirements.txt
```

## How to Install and Run
1. Install Python 3.8 or newer and check it with `python --version`
   (use `python3` on Linux/macOS).
2. Get the code:
   ```
   git clone https://github.com/Sakkkky/student-grade-manager.git
   cd student-grade-manager
   ```
3. No packages need to be installed (`requirements.txt` only says so).
4. Start the program:
   ```
   python main.py
   ```
5. Pick an option from the menu. A typical first run is: `1` (add student), `2` (add marks),
   `3` (view report card), `8` (class summary). Use `0` to exit.

Registration numbers look like `26BCE10842` (2 digits, 3 letters, 5 digits).

## How to Run the Tests
From the project root:
```
python -m unittest discover -s tests -t .
```
All tests should print `OK`.

## Grading Scale
| Marks | Grade | Points |
|-------|-------|--------|
| 90-100 | S | 10 |
| 80-89 | A | 9 |
| 70-79 | B | 8 |
| 60-69 | C | 7 |
| 50-59 | D | 6 |
| 40-49 | E | 5 |
| below 40 | F | 0 |

A student passes only if every subject is 40 or above.

## Screenshots
Add your own terminal screenshots here after running the program.
