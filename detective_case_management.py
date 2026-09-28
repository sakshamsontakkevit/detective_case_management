import ast
import os
from datetime import datetime
from typing import Dict, List, Optional


DATA_DIR = "data"
FILES = {
    "investigators": os.path.join(DATA_DIR, "investigators.txt"),
    "cases": os.path.join(DATA_DIR, "cases.txt"),
    "suspects": os.path.join(DATA_DIR, "suspects.txt"),
    "witnesses": os.path.join(DATA_DIR, "witnesses.txt"),
    "evidence": os.path.join(DATA_DIR, "evidence.txt"),
}


# ============================================================
# Utility Functions
# ============================================================

def ensure_data_directory():
    """Create the data folder and plain-text data files when needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for path in FILES.values():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                file.write("[]")


def load_data(path: str) -> list:
    """Read a list of Python data from a normal text file."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []
            data = ast.literal_eval(content)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, ValueError, SyntaxError):
        return []


def save_data(path: str, data: list):
    """Save application data as readable Python text, not JSON or SQL."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(repr(data))


def generate_id(prefix: str, records: list, field: str = "id") -> str:
    numbers = []
    for record in records:
        value = str(record.get(field, ""))
        if value.startswith(prefix):
            suffix = value[len(prefix):]
            if suffix.isdigit():
                numbers.append(int(suffix))
    number = max(numbers, default=0) + 1
    return f"{prefix}{number:04d}"


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def pause():
    input("\nPress Enter to continue...")


def line(char="=", width=72):
    print(char * width)


def header(title: str):
    print("\n")
    line()
    print(title.center(72))
    line()


def read_required(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_int(prompt: str, minimum=None, maximum=None) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            limits = []
            if minimum is not None:
                limits.append(f"minimum {minimum}")
            if maximum is not None:
                limits.append(f"maximum {maximum}")
            suffix = f" ({', '.join(limits)})" if limits else ""
            print(f"Enter a valid integer{suffix}.")


def confirm(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


# ============================================================
# Domain Classes
# ============================================================

class Person:
    def __init__(self, person_id, name, age, phone, email, address):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "age": self.age,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
        }


class Investigator(Person):
    def __init__(self, person_id, name, age, phone, email, address,
                 badge_number, rank, specialization, active=True):
        super().__init__(person_id, name, age, phone, email, address)
        self.badge_number = badge_number
        self.rank = rank
        self.specialization = specialization
        self.active = active

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "badge_number": self.badge_number,
            "rank": self.rank,
            "specialization": self.specialization,
            "active": self.active,
        })
        return data


class Suspect(Person):
    def __init__(self, person_id, name, age, phone, email, address,
                 occupation, risk_level, notes=""):
        super().__init__(person_id, name, age, phone, email, address)
        self.occupation = occupation
        self.risk_level = risk_level
        self.notes = notes

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "occupation": self.occupation,
            "risk_level": self.risk_level,
            "notes": self.notes,
        })
        return data


class Witness(Person):
    def __init__(self, person_id, name, age, phone, email, address,
                 statement, reliability="Unknown"):
        super().__init__(person_id, name, age, phone, email, address)
        self.statement = statement
        self.reliability = reliability

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "statement": self.statement,
            "reliability": self.reliability,
        })
        return data


class Evidence:
    VALID_TYPES = ["Physical", "Digital", "Documentary", "Photographic",
                   "Biological", "Financial", "Other"]
    VALID_STATUS = ["Collected", "Under Analysis", "Verified", "Disputed",
                    "Archived"]

    def __init__(self, evidence_id, case_id, title, evidence_type,
                 description, location, collected_by, collected_date,
                 status="Collected", chain_of_custody=None):
        self.evidence_id = evidence_id
        self.case_id = case_id
        self.title = title
        self.evidence_type = evidence_type
        self.description = description
        self.location = location
        self.collected_by = collected_by
        self.collected_date = collected_date
        self.status = status
        self.chain_of_custody = chain_of_custody or []

    def add_custody_entry(self, officer, action):
        self.chain_of_custody.append({
            "timestamp": now(),
            "officer": officer,
            "action": action,
        })

    def to_dict(self):
        return {
            "id": self.evidence_id,
            "case_id": self.case_id,
            "title": self.title,
            "evidence_type": self.evidence_type,
            "description": self.description,
            "location": self.location,
            "collected_by": self.collected_by,
            "collected_date": self.collected_date,
            "status": self.status,
            "chain_of_custody": self.chain_of_custody,
        }


class Case:
    VALID_STATUS = ["Open", "Under Investigation", "Solved", "Closed",
                    "Cold Case"]
    VALID_PRIORITY = ["Low", "Medium", "High", "Critical"]

    def __init__(self, case_id, title, category, description, location,
                 date_reported, priority="Medium", status="Open",
                 assigned_investigator=None, created_by="System",
                 solved_date=None):
        self.case_id = case_id
        self.title = title
        self.category = category
        self.description = description
        self.location = location
        self.date_reported = date_reported
        self.priority = priority
        self.status = status
        self.assigned_investigator = assigned_investigator
        self.created_by = created_by
        self.solved_date = solved_date
        self.suspects = []
        self.witnesses = []
        self.evidence = []
        self.notes = []
        self.timeline = [{
            "timestamp": date_reported,
            "event": "Case created",
            "by": created_by,
        }]

    def add_timeline_event(self, event, by="System"):
        self.timeline.append({
            "timestamp": now(),
            "event": event,
            "by": by,
        })

    def add_note(self, note, by="System"):
        self.notes.append({
            "timestamp": now(),
            "note": note,
            "by": by,
        })

    def add_suspect(self, suspect_id):
        if suspect_id not in self.suspects:
            self.suspects.append(suspect_id)

    def add_witness(self, witness_id):
        if witness_id not in self.witnesses:
            self.witnesses.append(witness_id)

    def add_evidence(self, evidence_id):
        if evidence_id not in self.evidence:
            self.evidence.append(evidence_id)

    def to_dict(self):
        return {
            "id": self.case_id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "location": self.location,
            "date_reported": self.date_reported,
            "priority": self.priority,
            "status": self.status,
            "assigned_investigator": self.assigned_investigator,
            "created_by": self.created_by,
            "solved_date": self.solved_date,
            "suspects": self.suspects,
            "witnesses": self.witnesses,
            "evidence": self.evidence,
            "notes": self.notes,
            "timeline": self.timeline,
        }


# ============================================================
# Repository Layer
# ============================================================

class DataRepository:
    """Handles persistent text-file storage for the application."""

    def __init__(self):
        ensure_data_directory()

    def load_investigators(self):
        return load_data(FILES["investigators"])

    def save_investigators(self, data):
        save_data(FILES["investigators"], data)

    def load_cases(self):
        return load_data(FILES["cases"])

    def save_cases(self, data):
        save_data(FILES["cases"], data)

    def load_suspects(self):
        return load_data(FILES["suspects"])

    def save_suspects(self, data):
        save_data(FILES["suspects"], data)

    def load_witnesses(self):
        return load_data(FILES["witnesses"])

    def save_witnesses(self, data):
        save_data(FILES["witnesses"], data)

    def load_evidence(self):
        return load_data(FILES["evidence"])

    def save_evidence(self, data):
        save_data(FILES["evidence"], data)

    def reset_all(self):
        for path in FILES.values():
            save_data(path, [])


# ============================================================
# Main Management System
# ============================================================

class DetectiveCaseManagementSystem:
    def __init__(self):
        self.repository = DataRepository()
        self.investigators = self.repository.load_investigators()
        self.cases = self.repository.load_cases()
        self.suspects = self.repository.load_suspects()
        self.witnesses = self.repository.load_witnesses()
        self.evidence = self.repository.load_evidence()

    # -------------------- Persistence --------------------

    def save_all(self):
        self.repository.save_investigators(self.investigators)
        self.repository.save_cases(self.cases)
        self.repository.save_suspects(self.suspects)
        self.repository.save_witnesses(self.witnesses)
        self.repository.save_evidence(self.evidence)

    # -------------------- Find Helpers --------------------

    def find_case(self, case_id):
        return next((c for c in self.cases if c["id"] == case_id), None)

    def find_investigator(self, investigator_id):
        return next((i for i in self.investigators if i["id"] == investigator_id), None)

    def find_suspect(self, suspect_id):
        return next((s for s in self.suspects if s["id"] == suspect_id), None)

    def find_witness(self, witness_id):
        return next((w for w in self.witnesses if w["id"] == witness_id), None)

    def find_evidence(self, evidence_id):
        return next((e for e in self.evidence if e["id"] == evidence_id), None)

    # -------------------- Investigator Management --------------------

    def add_investigator(self):
        header("REGISTER INVESTIGATOR")
        investigator_id = generate_id("INV", self.investigators)
        name = read_required("Full name: ")
        age = read_int("Age: ", 18, 80)
        phone = read_required("Phone: ")
        email = read_required("Email: ")
        address = read_required("Address: ")
        badge = read_required("Badge number: ")
        rank = read_required("Rank: ")
        specialization = read_required("Specialization: ")

        record = Investigator(
            investigator_id, name, age, phone, email, address,
            badge, rank, specialization
        ).to_dict()

        self.investigators.append(record)
        self.save_all()
        print(f"\nInvestigator registered successfully. ID: {investigator_id}")

    def list_investigators(self, active_only=False):
        records = self.investigators
        if active_only:
            records = [i for i in records if i.get("active", True)]

        if not records:
            print("No investigators found.")
            return

        for inv in records:
            assigned = sum(
                1 for case in self.cases
                if case.get("assigned_investigator") == inv["id"]
                and case.get("status") not in ("Closed", "Solved")
            )
            print(
                f'{inv["id"]} | {inv["name"]} | Badge: {inv["badge_number"]} | '
                f'{inv["rank"]} | {inv["specialization"]} | Active: '
                f'{inv.get("active", True)} | Active Cases: {assigned}'
            )

    def deactivate_investigator(self):
        header("DEACTIVATE INVESTIGATOR")
        self.list_investigators(True)
        investigator_id = read_required("Investigator ID: ")
        investigator = self.find_investigator(investigator_id)

        if not investigator:
            print("Investigator not found.")
            return

        investigator["active"] = False
        self.save_all()
        print("Investigator deactivated.")

    # -------------------- Case Management --------------------

    def create_case(self):
        header("CREATE NEW CASE")
        case_id = generate_id("CASE", self.cases)
        title = read_required("Case title: ")
        category = read_required("Category: ")
        description = read_required("Description: ")
        location = read_required("Incident location: ")

        print("\nPriority:")
        for index, value in enumerate(Case.VALID_PRIORITY, 1):
            print(f"{index}. {value}")
        priority = Case.VALID_PRIORITY[
            read_int("Choose priority: ", 1, len(Case.VALID_PRIORITY)) - 1
        ]

        investigator_id = input(
            "Assign investigator ID (leave blank for unassigned): "
        ).strip()

        if investigator_id and not self.find_investigator(investigator_id):
            print("Investigator not found. Case will remain unassigned.")
            investigator_id = None

        case = Case(
            case_id=case_id,
            title=title,
            category=category,
            description=description,
            location=location,
            date_reported=now(),
            priority=priority,
            assigned_investigator=investigator_id,
            created_by="System",
        )
        self.cases.append(case.to_dict())
        self.save_all()
        print(f"\nCase created successfully. Case ID: {case_id}")

    def list_cases(self, records=None):
        records = self.cases if records is None else records

        if not records:
            print("No cases found.")
            return

        for case in records:
            investigator = case.get("assigned_investigator") or "Unassigned"
            print(
                f'{case["id"]} | {case["title"][:28]:28} | '
                f'{case["category"][:15]:15} | '
                f'{case["priority"]:8} | {case["status"]:18} | '
                f'{investigator}'
            )

    def search_cases(self):
        header("SEARCH CASES")
        keyword = read_required("Enter keyword: ").lower()
        results = []

        for case in self.cases:
            searchable = " ".join([
                str(case.get("id", "")),
                str(case.get("title", "")),
                str(case.get("category", "")),
                str(case.get("description", "")),
                str(case.get("location", "")),
                str(case.get("status", "")),
                str(case.get("priority", "")),
            ]).lower()

            if keyword in searchable:
                results.append(case)

        self.list_cases(results)

    def filter_cases(self):
        header("FILTER CASES")
        print("1. By status")
        print("2. By priority")
        print("3. By category")
        print("4. Assigned investigator")
        choice = input("Choose: ").strip()

        if choice == "1":
            for i, status in enumerate(Case.VALID_STATUS, 1):
                print(f"{i}. {status}")
            status = Case.VALID_STATUS[
                read_int("Choose: ", 1, len(Case.VALID_STATUS)) - 1
            ]
            results = [c for c in self.cases if c["status"] == status]

        elif choice == "2":
            for i, priority in enumerate(Case.VALID_PRIORITY, 1):
                print(f"{i}. {priority}")
            priority = Case.VALID_PRIORITY[
                read_int("Choose: ", 1, len(Case.VALID_PRIORITY)) - 1
            ]
            results = [c for c in self.cases if c["priority"] == priority]

        elif choice == "3":
            category = read_required("Category: ").lower()
            results = [
                c for c in self.cases
                if category in c["category"].lower()
            ]

        elif choice == "4":
            investigator_id = read_required("Investigator ID: ")
            results = [
                c for c in self.cases
                if c.get("assigned_investigator") == investigator_id
            ]

        else:
            print("Invalid choice.")
            return

        self.list_cases(results)

    def update_case_status(self):
        header("UPDATE CASE STATUS")
        case_id = read_required("Case ID: ")
        case = self.find_case(case_id)

        if not case:
            print("Case not found.")
            return

        for i, status in enumerate(Case.VALID_STATUS, 1):
            print(f"{i}. {status}")

        status = Case.VALID_STATUS[
            read_int("New status: ", 1, len(Case.VALID_STATUS)) - 1
        ]
        case["status"] = status

        if status == "Solved":
            case["solved_date"] = today()

        case.setdefault("timeline", []).append({
            "timestamp": now(),
            "event": f"Status changed to {status}",
            "by": "System",
        })
        self.save_all()
        print("Case status updated.")

    def assign_case(self):
        header("ASSIGN CASE")
        case_id = read_required("Case ID: ")
        case = self.find_case(case_id)

        if not case:
            print("Case not found.")
            return

        self.list_investigators(True)
        investigator_id = read_required("Investigator ID: ")

        if not self.find_investigator(investigator_id):
            print("Investigator not found.")
            return

        case["assigned_investigator"] = investigator_id
        case.setdefault("timeline", []).append({
            "timestamp": now(),
            "event": f"Assigned to investigator {investigator_id}",
            "by": "System",
        })

        if case["status"] == "Open":
            case["status"] = "Under Investigation"

        self.save_all()
        print("Case assigned successfully.")

    # -------------------- Suspect Management --------------------

    def add_suspect(self):
        header("REGISTER SUSPECT")
        suspect_id = generate_id("SUS", self.suspects)
        name = read_required("Full name: ")
        age = read_int("Age: ", 1, 120)
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()
        address = read_required("Address: ")
        occupation = read_required("Occupation: ")

        print("Risk level:")
        levels = ["Low", "Medium", "High", "Critical"]
        for i, value in enumerate(levels, 1):
            print(f"{i}. {value}")
        risk = levels[read_int("Choose: ", 1, 4) - 1]
        notes = input("Initial notes: ").strip()

        record = Suspect(
            suspect_id, name, age, phone, email, address,
            occupation, risk, notes
        ).to_dict()

        self.suspects.append(record)
        self.save_all()

        print(f"Suspect registered. ID: {suspect_id}")

    def link_suspect_to_case(self):
        header("LINK SUSPECT TO CASE")
        case_id = read_required("Case ID: ")
        case = self.find_case(case_id)
        if not case:
            print("Case not found.")
            return

        self.list_suspects()
        suspect_id = read_required("Suspect ID: ")

        if not self.find_suspect(suspect_id):
            print("Suspect not found.")
            return

        if suspect_id not in case.setdefault("suspects", []):
            case["suspects"].append(suspect_id)

        case.setdefault("timeline", []).append({
            "timestamp": now(),
            "event": f"Suspect {suspect_id} linked to case",
            "by": "System",
        })
        self.save_all()
        print("Suspect linked successfully.")

    def list_suspects(self):
        if not self.suspects:
            print("No suspects registered.")
            return
        for suspect in self.suspects:
            print(
                f'{suspect["id"]} | {suspect["name"]} | Age {suspect["age"]} | '
                f'Occupation: {suspect["occupation"]} | '
                f'Risk: {suspect["risk_level"]}'
            )

    # -------------------- Witness Management --------------------

    def add_witness(self):
        header("REGISTER WITNESS")
        witness_id = generate_id("WIT", self.witnesses)
        name = read_required("Full name: ")
        age = read_int("Age: ", 1, 120)
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()
        address = read_required("Address: ")
        statement = read_required("Statement: ")

        reliability_options = ["Unknown", "Low", "Medium", "High"]
        for i, value in enumerate(reliability_options, 1):
            print(f"{i}. {value}")
        reliability = reliability_options[
            read_int("Reliability: ", 1, 4) - 1
        ]

        record = Witness(
            witness_id, name, age, phone, email, address,
            statement, reliability
        ).to_dict()

        self.witnesses.append(record)
        self.save_all()
        print(f"Witness registered. ID: {witness_id}")

    def link_witness_to_case(self):
        header("LINK WITNESS TO CASE")
        case_id = read_required("Case ID: ")
        case = self.find_case(case_id)
        if not case:
            print("Case not found.")
            return

        self.list_witnesses()
        witness_id = read_required("Witness ID: ")

        if not self.find_witness(witness_id):
            print("Witness not found.")
            return

        if witness_id not in case.setdefault("witnesses", []):
            case["witnesses"].append(witness_id)

        case.setdefault("timeline", []).append({
            "timestamp": now(),
            "event": f"Witness {witness_id} linked to case",
            "by": "System",
        })
        self.save_all()
        print("Witness linked successfully.")

    def list_witnesses(self):
        if not self.witnesses:
            print("No witnesses registered.")
            return
        for witness in self.witnesses:
            print(
                f'{witness["id"]} | {witness["name"]} | Age {witness["age"]} | '
                f'Reliability: {witness["reliability"]}'
            )

    # -------------------- Evidence Management --------------------

    def add_evidence(self):
        header("REGISTER EVIDENCE")
        case_id = read_required("Case ID: ")
        case = self.find_case(case_id)

        if not case:
            print("Case not found.")
            return

        evidence_id = generate_id("EVD", self.evidence)
        title = read_required("Evidence title: ")

        for i, value in enumerate(Evidence.VALID_TYPES, 1):
            print(f"{i}. {value}")
        evidence_type = Evidence.VALID_TYPES[
            read_int("Evidence type: ", 1, len(Evidence.VALID_TYPES)) - 1
        ]

        description = read_required("Description: ")
        location = read_required("Collected from: ")
        collected_by = read_required("Collected by: ")

        evidence = Evidence(
            evidence_id=evidence_id,
            case_id=case_id,
            title=title,
            evidence_type=evidence_type,
            description=description,
            location=location,
            collected_by=collected_by,
            collected_date=now(),
        )
        evidence.add_custody_entry(collected_by, "Evidence collected")

        self.evidence.append(evidence.to_dict())
        case.setdefault("evidence", []).append(evidence_id)
        case.setdefault("timeline", []).append({
            "timestamp": now(),
            "event": f"Evidence {evidence_id} added",
            "by": collected_by,
        })

        self.save_all()
        print(f"Evidence registered. ID: {evidence_id}")

    def update_evidence_status(self):
        header("UPDATE EVIDENCE STATUS")
        evidence_id = read_required("Evidence ID: ")
        evidence = self.find_evidence(evidence_id)

        if not evidence:
            print("Evidence not found.")
            return

        for i, status in enumerate(Evidence.VALID_STATUS, 1):
            print(f"{i}. {status}")
        status = Evidence.VALID_STATUS[
            read_int("New status: ", 1, len(Evidence.VALID_STATUS)) - 1
        ]

        officer = read_required("Officer handling evidence: ")
        evidence["status"] = status
        evidence.setdefault("chain_of_custody", []).append({
            "timestamp": now(),
            "officer": officer,
            "action": f"Status changed to {status}",
        })

        self.save_all()
        print("Evidence status updated.")

    def list_evidence(self, case_id=None):
        records = self.evidence
        if case_id:
            records = [e for e in records if e["case_id"] == case_id]

        if not records:
            print("No evidence found.")
            return

        for evidence in records:
            print(
                f'{evidence["id"]} | {evidence["title"][:25]:25} | '
                f'{evidence["evidence_type"]:15} | '
                f'{evidence["status"]:15} | Case: {evidence["case_id"]}'
            )

    # -------------------- Notes and Reports --------------------

    def add_case_note(self):
        header("ADD CASE NOTE")
        case_id = read_required("Case ID: ")
        case = self.find_case(case_id)

        if not case:
            print("Case not found.")
            return

        note = read_required("Note: ")
        author = input("Author: ").strip() or "System"

        case.setdefault("notes", []).append({
            "timestamp": now(),
            "note": note,
            "by": author,
        })
        case.setdefault("timeline", []).append({
            "timestamp": now(),
            "event": "Case note added",
            "by": author,
        })
        self.save_all()
        print("Note added.")

    def show_case_details(self):
        header("CASE DETAILS")
        case_id = read_required("Case ID: ")
        case = self.find_case(case_id)

        if not case:
            print("Case not found.")
            return

        print(f'Case ID       : {case["id"]}')
        print(f'Title         : {case["title"]}')
        print(f'Category      : {case["category"]}')
        print(f'Description   : {case["description"]}')
        print(f'Location      : {case["location"]}')
        print(f'Reported      : {case["date_reported"]}')
        print(f'Priority      : {case["priority"]}')
        print(f'Status        : {case["status"]}')
        print(f'Investigator  : {case.get("assigned_investigator") or "Unassigned"}')
        print(f'Solved Date   : {case.get("solved_date") or "-"}')

        print("\nSuspects:")
        if case.get("suspects"):
            for suspect_id in case["suspects"]:
                suspect = self.find_suspect(suspect_id)
                print(f'  - {suspect_id}: {suspect["name"] if suspect else "Unknown"}')
        else:
            print("  None")

        print("\nWitnesses:")
        if case.get("witnesses"):
            for witness_id in case["witnesses"]:
                witness = self.find_witness(witness_id)
                print(f'  - {witness_id}: {witness["name"] if witness else "Unknown"}')
        else:
            print("  None")

        print("\nEvidence:")
        if case.get("evidence"):
            for evidence_id in case["evidence"]:
                evidence = self.find_evidence(evidence_id)
                if evidence:
                    print(
                        f'  - {evidence_id}: {evidence["title"]} '
                        f'[{evidence["status"]}]'
                    )
        else:
            print("  None")

        print("\nNotes:")
        for note in case.get("notes", []):
            print(f'  [{note["timestamp"]}] {note["by"]}: {note["note"]}')

        print("\nTimeline:")
        for event in case.get("timeline", []):
            print(f'  [{event["timestamp"]}] {event["event"]} ({event["by"]})')

    def generate_case_report(self):
        header("GENERATE CASE REPORT")
        case_id = read_required("Case ID: ")
        case = self.find_case(case_id)

        if not case:
            print("Case not found.")
            return

        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        path = os.path.join(report_dir, f"{case_id}_report.txt")

        investigator = self.find_investigator(
            case.get("assigned_investigator")
        )

        lines = [
            "=" * 80,
            "DETECTIVE CASE MANAGEMENT SYSTEM".center(80),
            "OFFICIAL CASE REPORT".center(80),
            "=" * 80,
            "",
            f"Case ID: {case['id']}",
            f"Title: {case['title']}",
            f"Category: {case['category']}",
            f"Location: {case['location']}",
            f"Date Reported: {case['date_reported']}",
            f"Priority: {case['priority']}",
            f"Status: {case['status']}",
            f"Assigned Investigator: "
            f"{investigator['name'] if investigator else 'Unassigned'}",
            "",
            "DESCRIPTION",
            "-" * 80,
            case["description"],
            "",
            "SUSPECTS",
            "-" * 80,
        ]

        for suspect_id in case.get("suspects", []):
            suspect = self.find_suspect(suspect_id)
            if suspect:
                lines.append(
                    f'{suspect["id"]} | {suspect["name"]} | '
                    f'Risk: {suspect["risk_level"]}'
                )

        lines.extend(["", "WITNESSES", "-" * 80])
        for witness_id in case.get("witnesses", []):
            witness = self.find_witness(witness_id)
            if witness:
                lines.append(
                    f'{witness["id"]} | {witness["name"]} | '
                    f'Reliability: {witness["reliability"]}'
                )

        lines.extend(["", "EVIDENCE", "-" * 80])
        for evidence_id in case.get("evidence", []):
            evidence = self.find_evidence(evidence_id)
            if evidence:
                lines.append(
                    f'{evidence["id"]} | {evidence["title"]} | '
                    f'{evidence["evidence_type"]} | {evidence["status"]}'
                )

        lines.extend(["", "TIMELINE", "-" * 80])
        for event in case.get("timeline", []):
            lines.append(
                f'[{event["timestamp"]}] {event["event"]} - {event["by"]}'
            )

        lines.extend([
            "",
            "=" * 80,
            f"Generated: {now()}",
            "=" * 80,
        ])

        with open(path, "w", encoding="utf-8") as file:
            file.write("\n".join(lines))

        print(f"Report generated: {path}")

    # -------------------- Dashboard --------------------

    def dashboard(self):
        header("INVESTIGATION DASHBOARD")

        total_cases = len(self.cases)
        open_cases = sum(c["status"] == "Open" for c in self.cases)
        investigation_cases = sum(
            c["status"] == "Under Investigation" for c in self.cases
        )
        solved_cases = sum(c["status"] == "Solved" for c in self.cases)
        closed_cases = sum(c["status"] == "Closed" for c in self.cases)
        cold_cases = sum(c["status"] == "Cold Case" for c in self.cases)
        critical_cases = sum(c["priority"] == "Critical" for c in self.cases)

        print(f"Total Cases             : {total_cases}")
        print(f"Open Cases              : {open_cases}")
        print(f"Under Investigation     : {investigation_cases}")
        print(f"Solved Cases            : {solved_cases}")
        print(f"Closed Cases            : {closed_cases}")
        print(f"Cold Cases              : {cold_cases}")
        print(f"Critical Priority Cases : {critical_cases}")
        print(f"Investigators            : {len(self.investigators)}")
        print(f"Registered Suspects      : {len(self.suspects)}")
        print(f"Registered Witnesses     : {len(self.witnesses)}")
        print(f"Evidence Records         : {len(self.evidence)}")

        if total_cases:
            resolution_rate = (solved_cases / total_cases) * 100
            print(f"Resolution Rate          : {resolution_rate:.2f}%")

        print("\nCases by category:")
        categories = {}
        for case in self.cases:
            categories[case["category"]] = categories.get(
                case["category"], 0
            ) + 1
        if categories:
            for category, count in sorted(categories.items()):
                print(f"  {category}: {count}")
        else:
            print("  No data.")

    # -------------------- Seed Data --------------------

    def load_demo_data(self):
        if any([
            self.investigators, self.cases, self.suspects,
            self.witnesses, self.evidence
        ]):
            print("Demo data is only loaded when all data files are empty.")
            return

        investigator = Investigator(
            "INV0001", "Arjun Mehta", 34, "9000000001",
            "arjun@example.com", "Central District",
            "D-1042", "Inspector", "Major Crimes"
        ).to_dict()

        investigator2 = Investigator(
            "INV0002", "Maya Rao", 31, "9000000002",
            "maya@example.com", "North District",
            "D-1088", "Detective", "Cyber Crime"
        ).to_dict()

        suspect = Suspect(
            "SUS0001", "Rohan Verma", 29, "9000000010",
            "rohan@example.com", "East Avenue",
            "Freelancer", "High", "Person of interest."
        ).to_dict()

        witness = Witness(
            "WIT0001", "Neha Sharma", 27, "9000000020",
            "neha@example.com", "Lake Road",
            "Saw a vehicle leaving the area at approximately 22:15.",
            "High"
        ).to_dict()

        case = Case(
            "CASE0001",
            "Midnight Warehouse Incident",
            "Theft",
            "High-value electronic equipment was reported missing.",
            "Industrial Area",
            "2026-09-20 22:30:00",
            "High",
            "Under Investigation",
            "INV0001",
            "System"
        )
        case.suspects = ["SUS0001"]
        case.witnesses = ["WIT0001"]
        case.add_timeline_event(
            "Suspect SUS0001 linked to case", "System"
        )

        evidence = Evidence(
            "EVD0001", "CASE0001", "Security Camera Footage",
            "Digital",
            "Camera recording from the loading dock.",
            "Warehouse entrance",
            "INV0001",
            "2026-09-21 09:10:00",
            "Verified"
        )
        evidence.add_custody_entry(
            "INV0001", "Evidence verified and secured"
        )

        self.investigators.extend([investigator, investigator2])
        self.suspects.append(suspect)
        self.witnesses.append(witness)
        self.cases.append(case.to_dict())
        self.evidence.append(evidence.to_dict())
        self.save_all()

        print("Demo data loaded successfully.")

    # -------------------- Menus --------------------

    def investigator_menu(self):
        while True:
            header("INVESTIGATOR MANAGEMENT")
            print("1. Register investigator")
            print("2. List investigators")
            print("3. List active investigators")
            print("4. Deactivate investigator")
            print("5. Back")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.add_investigator()
            elif choice == "2":
                self.list_investigators()
            elif choice == "3":
                self.list_investigators(True)
            elif choice == "4":
                self.deactivate_investigator()
            elif choice == "5":
                break
            else:
                print("Invalid option.")
            pause()

    def case_menu(self):
        while True:
            header("CASE MANAGEMENT")
            print("1. Create case")
            print("2. List all cases")
            print("3. Search cases")
            print("4. Filter cases")
            print("5. Show case details")
            print("6. Assign investigator")
            print("7. Update case status")
            print("8. Add case note")
            print("9. Generate case report")
            print("10. Back")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.create_case()
            elif choice == "2":
                self.list_cases()
            elif choice == "3":
                self.search_cases()
            elif choice == "4":
                self.filter_cases()
            elif choice == "5":
                self.show_case_details()
            elif choice == "6":
                self.assign_case()
            elif choice == "7":
                self.update_case_status()
            elif choice == "8":
                self.add_case_note()
            elif choice == "9":
                self.generate_case_report()
            elif choice == "10":
                break
            else:
                print("Invalid option.")
            pause()

    def suspect_menu(self):
        while True:
            header("SUSPECT MANAGEMENT")
            print("1. Register suspect")
            print("2. List suspects")
            print("3. Link suspect to case")
            print("4. Back")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.add_suspect()
            elif choice == "2":
                self.list_suspects()
            elif choice == "3":
                self.link_suspect_to_case()
            elif choice == "4":
                break
            else:
                print("Invalid option.")
            pause()

    def witness_menu(self):
        while True:
            header("WITNESS MANAGEMENT")
            print("1. Register witness")
            print("2. List witnesses")
            print("3. Link witness to case")
            print("4. Back")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.add_witness()
            elif choice == "2":
                self.list_witnesses()
            elif choice == "3":
                self.link_witness_to_case()
            elif choice == "4":
                break
            else:
                print("Invalid option.")
            pause()

    def evidence_menu(self):
        while True:
            header("EVIDENCE MANAGEMENT")
            print("1. Register evidence")
            print("2. List all evidence")
            print("3. List evidence for case")
            print("4. Update evidence status")
            print("5. Back")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.add_evidence()
            elif choice == "2":
                self.list_evidence()
            elif choice == "3":
                case_id = read_required("Case ID: ")
                self.list_evidence(case_id)
            elif choice == "4":
                self.update_evidence_status()
            elif choice == "5":
                break
            else:
                print("Invalid option.")
            pause()

    def run(self):
        ensure_data_directory()

        while True:
            header("DETECTIVE CASE MANAGEMENT SYSTEM")
            print("1. Investigation Dashboard")
            print("2. Case Management")
            print("3. Investigator Management")
            print("4. Suspect Management")
            print("5. Witness Management")
            print("6. Evidence Management")
            print("7. Load Demo Data")
            print("8. Save All Data")
            print("9. Exit")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.dashboard()
                pause()
            elif choice == "2":
                self.case_menu()
            elif choice == "3":
                self.investigator_menu()
            elif choice == "4":
                self.suspect_menu()
            elif choice == "5":
                self.witness_menu()
            elif choice == "6":
                self.evidence_menu()
            elif choice == "7":
                self.load_demo_data()
                pause()
            elif choice == "8":
                self.save_all()
                print("All data saved.")
                pause()
            elif choice == "9":
                self.save_all()
                print("\nAll data saved. Goodbye, Detective.")
                break
            else:
                print("Invalid option.")
                pause()


if __name__ == "__main__":
    system = DetectiveCaseManagementSystem()
    system.run()
