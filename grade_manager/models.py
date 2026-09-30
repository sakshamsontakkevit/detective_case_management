"""Data classes for the project (the OOP part)."""


class Student:
    """One student with a dictionary of subject -> marks."""

    def __init__(self, reg_no, name, marks=None):
        self.reg_no = reg_no
        self.name = name
        self.marks = marks if marks is not None else {}

    def set_mark(self, subject, mark):
        self.marks[subject] = mark

    def remove_mark(self, subject):
        return self.marks.pop(subject, None)

    def average(self):
        if not self.marks:
            return 0.0
        return sum(self.marks.values()) / len(self.marks)

    def to_dict(self):
        return {"reg_no": self.reg_no, "name": self.name, "marks": self.marks}

    @classmethod
    def from_dict(cls, data):
        return cls(data["reg_no"], data["name"], dict(data.get("marks", {})))

    def __str__(self):
        return f"{self.reg_no} - {self.name}"

    def __repr__(self):
        return f"Student({self.reg_no!r}, {self.name!r}, {self.marks!r})"
