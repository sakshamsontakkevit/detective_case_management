# Detective Case Management System

A console-based **Python Object-Oriented Programming (OOP)** project for managing fictional investigation cases.

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
- Automatic JSON data persistence
- Text case-report generation
- Demo/sample data
- Input validation and exception handling
- No third-party Python packages required

## OOP Concepts Demonstrated

### Encapsulation
Data and behavior are grouped inside classes such as `Case`, `Evidence`, `Person`, and `DetectiveCaseManagementSystem`.

### Inheritance
`Investigator`, `Suspect`, and `Witness` inherit common attributes and behavior from the `Person` class.

### Polymorphism
Each specialized person class overrides `to_dict()` to extend the serialized representation of the base class.

### Abstraction
`DataRepository` hides the details of reading and writing JSON files from the management system.

## Project Structure

```text
Detective-Case-Management-System/
│
├── detective_case_management.py
├── data/
│   ├── cases.json
│   ├── evidence.json
│   ├── investigators.json
│   ├── suspects.json
│   └── witnesses.json
├── reports/
│   └── generated case reports appear here
├── README.md
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.9 or newer
- No external packages

## How to Run

Open a terminal in the project directory:

```bash
python detective_case_management.py
```

On some systems:

```bash
python3 detective_case_management.py
```

## First Run

The application automatically creates the `data` directory and JSON database files.

You can select:

```text
7. Load Demo Data
```

to populate the system with fictional sample records.

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

### Evidence Management
Allows:
- Evidence registration
- Evidence type classification
- Evidence status updates
- Chain-of-custody records
- Case-to-evidence relationships

## Data Storage

The project uses JSON files as a lightweight local database. Data remains available after the application is closed.

No internet connection or database server is required.

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

## Important Note

This project is an educational simulation. All sample investigation records are fictional.
