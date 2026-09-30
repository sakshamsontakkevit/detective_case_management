"""Small helper functions that check user input before we use it."""
import re

from .errors import ValidationError

REG_NO_PATTERN = re.compile(r"^\d{2}[A-Z]{3}\d{5}$")  # e.g. 26BCE10842


def validate_reg_no(reg_no):
    reg_no = reg_no.strip().upper()
    if not REG_NO_PATTERN.match(reg_no):
        raise ValidationError("Reg. no must look like 26BCE10842.")
    return reg_no


def validate_name(name):
    name = name.strip()
    if len(name) < 2 or not all(ch.isalpha() or ch == " " for ch in name):
        raise ValidationError("Name must have letters and spaces only.")
    return name.title()


def validate_subject(subject):
    subject = subject.strip()
    if not subject:
        raise ValidationError("Subject name cannot be empty.")
    return subject.title()


def validate_mark(text):
    try:
        mark = float(text)
    except ValueError:
        raise ValidationError("Marks must be a number.")
    if mark < 0 or mark > 100:
        raise ValidationError("Marks must be between 0 and 100.")
    return mark
