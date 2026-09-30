"""Turns marks into letter grades and grade points."""


class GradeCalculator:
    # (minimum mark, letter, grade point) - checked from top to bottom
    SCALE = [
        (90, "S", 10),
        (80, "A", 9),
        (70, "B", 8),
        (60, "C", 7),
        (50, "D", 6),
        (40, "E", 5),
    ]
    PASS_MARK = 40

    @classmethod
    def letter(cls, mark):
        for minimum, letter, _ in cls.SCALE:
            if mark >= minimum:
                return letter
        return "F"

    @classmethod
    def point(cls, mark):
        for minimum, _, point in cls.SCALE:
            if mark >= minimum:
                return point
        return 0

    @classmethod
    def gpa(cls, marks):
        """Simple average of grade points over all subjects."""
        if not marks:
            return 0.0
        points = [cls.point(m) for m in marks.values()]
        return sum(points) / len(points)

    @classmethod
    def has_passed(cls, marks):
        return bool(marks) and all(m >= cls.PASS_MARK for m in marks.values())
