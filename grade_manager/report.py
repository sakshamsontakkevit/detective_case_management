"""Builds the text that gets printed on screen (tables and report cards)."""
from .grading import GradeCalculator


def report_card(student):
    lines = [
        "=" * 44,
        f"REPORT CARD: {student.name} ({student.reg_no})",
        "=" * 44,
        f"{'Subject':<20}{'Marks':>8}{'Grade':>8}",
        "-" * 44,
    ]
    for subject, mark in sorted(student.marks.items()):
        lines.append(f"{subject:<20}{mark:>8.1f}{GradeCalculator.letter(mark):>8}")
    if not student.marks:
        lines.append("No marks entered yet.")
    else:
        result = "PASS" if GradeCalculator.has_passed(student.marks) else "FAIL"
        lines += [
            "-" * 44,
            f"Average : {student.average():.2f}",
            f"GPA     : {GradeCalculator.gpa(student.marks):.2f}",
            f"Result  : {result}",
        ]
    lines.append("=" * 44)
    return "\n".join(lines)


def student_table(students):
    if not students:
        return "No students to show."
    lines = [f"{'Rank':<6}{'Reg No':<14}{'Name':<22}{'Avg':>7}{'GPA':>6}",
             "-" * 55]
    for rank, s in enumerate(students, start=1):
        lines.append(
            f"{rank:<6}{s.reg_no:<14}{s.name[:20]:<22}"
            f"{s.average():>7.2f}{GradeCalculator.gpa(s.marks):>6.2f}"
        )
    return "\n".join(lines)


def class_summary(manager):
    total = len(manager.students)
    lines = ["CLASS SUMMARY", "-" * 30,
             f"Students       : {total}",
             f"Class average  : {manager.class_average():.2f}",
             f"Passed         : {manager.pass_count()} / {total}",
             "Subject averages:"]
    averages = manager.subject_averages()
    if not averages:
        lines.append("  (no marks yet)")
    for subject, avg in sorted(averages.items()):
        lines.append(f"  {subject:<18}{avg:>6.2f}")
    return "\n".join(lines)
