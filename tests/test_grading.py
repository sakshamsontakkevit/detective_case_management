import unittest

from grade_manager.grading import GradeCalculator


class GradingTests(unittest.TestCase):
    def test_letters(self):
        self.assertEqual(GradeCalculator.letter(95), "S")
        self.assertEqual(GradeCalculator.letter(80), "A")
        self.assertEqual(GradeCalculator.letter(39.9), "F")

    def test_gpa(self):
        self.assertEqual(GradeCalculator.gpa({"a": 95, "b": 75}), 9.0)
        self.assertEqual(GradeCalculator.gpa({}), 0.0)

    def test_pass_fail(self):
        self.assertTrue(GradeCalculator.has_passed({"a": 40, "b": 90}))
        self.assertFalse(GradeCalculator.has_passed({"a": 39, "b": 90}))
        self.assertFalse(GradeCalculator.has_passed({}))


if __name__ == "__main__":
    unittest.main()
