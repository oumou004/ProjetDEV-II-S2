import unittest

from classes.subject import Subject


class TestSubject(unittest.TestCase):
    def setUp(self):
        self.subject = Subject()
        self.subject_name = "__test_subject_unit__"

    def tearDown(self):
        subject_id = self.subject.get_subject_id(self.subject_name)
        if subject_id != -1:
            self.subject.remove_subject(subject_id)
        self.subject.close()

    def test_add_find_and_remove_subject(self):
        self.subject.add_subject(self.subject_name)

        subject_id = self.subject.get_subject_id(self.subject_name)
        subjects = self.subject.get_subjects()

        self.assertNotEqual(subject_id, -1)
        self.assertIn((subject_id, self.subject_name), subjects)

        self.subject.remove_subject(subject_id)
        self.assertEqual(self.subject.get_subject_id(self.subject_name), -1)


if __name__ == "__main__":
    unittest.main()
