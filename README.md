# Detective Case Management System

A command-line **Python Object-Oriented Programming (OOP)** project for managing fictional investigation cases.

The project is built using Python fundamentals, OOP, collections, functions, exception handling, and basic file handling. It does not require SQL, a database server, or third-party packages.

## Features

- Investigator registration and management
- Case creation and assignment
- Case status and priority management
- Case search and filtering
- Suspect registration and case linking
- Witness registration and case linking
- Evidence management
- Evidence chain-of-custody tracking
- Case notes and investigation timeline
- Investigation dashboard and statistics
- Plain-text file persistence
- Text case-report generation
- Demo/sample data
- Input validation and exception handling
- Fully command-line based

## OOP Concepts Demonstrated

### Encapsulation
Data and related operations are grouped inside classes such as `Case`, `Evidence`, `Person`, and `DetectiveCaseManagementSystem`.

### Inheritance
`Investigator`, `Suspect`, and `Witness` inherit common attributes and methods from the `Person` class.

### Polymorphism
The specialized person classes override `to_dict()` to add their own information while keeping the common `Person` structure.

### Abstraction
`DataRepository` handles file storage so the main management system does not need to deal with file operations directly.

## Project Structure

```text
Detective-Case-Management-System/
│
├── detective_case_management.py
├── data/
│   ├── cases.txt
│   ├── evidence.txt
│   ├── investigators.txt
│   ├── suspects.txt
│   └── witnesses.txt
├── reports/
│   └── generated case reports appear here
├── README.md
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.9 or newer
- No external packages
- No SQL/database server
- No internet connection required

## Setup

### 1. Install Python

Install Python 3.9 or newer if it is not already installed.

Check the installation:

```bash
python --version
```

On some systems:

```bash
python3 --version
```

### 2. Open the project folder

Open a terminal inside the project directory:

```bash
cd Detective-Case-Management-System
```

### 3. Install dependencies

There are no third-party dependencies. The project uses Python's standard library only.

The `requirements.txt` file is included for completeness and contains no external packages.

## Run the Project

Run the following command:

```bash
python detective_case_management.py
```

On systems using `python3`:

```bash
python3 detective_case_management.py
```

The application starts directly in the terminal.

## First Run

The program automatically creates the `data` folder and the required `.txt` files if they do not already exist.

From the main menu, option **7 - Load Demo Data** can be used to insert fictional sample records.

## Data Storage

The project uses normal `.txt` files for local data persistence. Python writes the application data to these files and reads it again when the program starts.

Example:

```text
 data/cases.txt
 data/investigators.txt
 data/suspects.txt
 data/witnesses.txt
 data/evidence.txt
```

This keeps the project simple and avoids requiring SQL or an external database server.

## Main Modules

### Dashboard

Shows:

- Total cases
- Open cases
- Cases under investigation
- Solved cases
- Closed cases
- Cold cases
- Critical cases
- Number of investigators
- Number of suspects
- Number of witnesses
- Number of evidence records
- Resolution rate
- Cases grouped by category

### Case Management

Allows users to:

- Create cases
- List cases
- Search cases
- Filter cases
- View complete case details
- Assign investigators
- Update case status
- Add investigation notes
- Generate text reports

### Investigator Management

Allows users to:

- Register investigators
- View investigators
- Deactivate investigators
- Track assigned active cases

### Suspect Management

Allows users to:

- Register suspects
- List suspects
- Link suspects to cases

### Witness Management

Allows users to:

- Register witnesses
- Store witness statements
- Record reliability
- Link witnesses to cases

### Evidence Management

Allows users to:

- Register evidence
- Classify evidence
- Update evidence status
- Track chain of custody
- Link evidence to cases

## Example Workflow

1. Register an investigator.
2. Create a new case.
3. Assign the investigator.
4. Register a suspect.
5. Link the suspect to the case.
6. Register a witness.
7. Link the witness to the case.
8. Register evidence.
9. Update evidence status.
10. Add investigation notes.
11. Change the case status.
12. Generate the final case report.

## Generated Reports

When a case report is generated, it is saved as a `.txt` file inside the `reports` directory.

For example:

```text
reports/CASE0001_report.txt
```

## Command-Line Execution

The complete project runs through the terminal. No graphical interface or separate application setup is required.

## Important Note

This project is an educational simulation. All sample investigation records are fictional.
