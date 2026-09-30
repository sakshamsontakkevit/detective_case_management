"""Saves and loads students from a JSON file (plain file handling)."""
import json
import logging
import os

from .models import Student

log = logging.getLogger(__name__)


class FileStorage:
    def __init__(self, path):
        self.path = path

    def load(self):
        """Return a dict of reg_no -> Student. Empty dict if no file yet."""
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            students = [Student.from_dict(item) for item in raw]
        except (json.JSONDecodeError, KeyError, TypeError) as err:
            log.error("Could not read %s: %s", self.path, err)
            print("Warning: data file is damaged, starting with an empty list.")
            return {}
        log.info("Loaded %d students", len(students))
        return {s.reg_no: s for s in students}

    def save(self, students):
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=2)
        log.info("Saved %d students", len(students))
