# fmt: off
import pytest
from .task import TrackerApplication, Student, Course


class TestTracker:
    @pytest.fixture(autouse=True)
    def setup_tracker(self):
        self.tracker = TrackerApplication()

    def test_correct_credentials(self):
        assert self.tracker.validate_credentials(["John", "Middle", "Smith", "email@dot.com"]) is not None
        assert self.tracker.validate_credentials(["John", "Smith", "email@dot.com"]) is not None
        assert self.tracker.validate_credentials(["Jane", "Doe", "j@doe.com"]) is not None

    def test_incorrect_number_of_credential_fields(self):
        assert self.tracker.validate_credentials([]) is None
        assert self.tracker.validate_credentials(["John"]) is None
        assert self.tracker.validate_credentials(["John", "Smith"]) is None
        assert self.tracker.validate_credentials(["John", "email@example.com"]) is None

    def test_valid_email(self):
        assert self.tracker.validate_email("email@example.com")
        assert self.tracker.validate_email("email@example.co.uk")
        assert self.tracker.validate_email("name.surname@example.com")

    def test_invalid_email(self):
        assert not self.tracker.validate_email("name@surname@example.com")
        assert not self.tracker.validate_email("email@example")
        assert not self.tracker.validate_email("name.surname@.com")
        assert not self.tracker.validate_email("@example.com")

    def test_valid_name(self):
        assert self.tracker.validate_name("John")
        assert self.tracker.validate_name("Jean-Claude")
        assert self.tracker.validate_name("O'Neill")
        assert self.tracker.validate_name("Louis XVI")

    def test_invalid_name(self):
        assert not self.tracker.validate_name("John'")
        assert not self.tracker.validate_name("Jean -Claude")
        assert not self.tracker.validate_name("O-'Neill")
        assert not self.tracker.validate_name("John S")
        assert not self.tracker.validate_name("Stanisław Oğuz")

    def test_invalid_points_string(self):
        tracker = TrackerApplication()
        student = Student("John", "Doe", "john@doe.com")
        tracker.students[student.student_id] = student
        assert not tracker.validate_points_string("100 1 2 3 4")
        assert not tracker.validate_points_string("abcd 1 2 3 4")
        assert not tracker.validate_points_string("")
        assert not tracker.validate_points_string("10000 1 2 3")
        assert not tracker.validate_points_string("10000 1 2 3 4 5")
        assert not tracker.validate_points_string("10000 -1 2 3 4")
        assert not tracker.validate_points_string("10000 a b c d")

    def test_valid_points_string(self):
        tracker = TrackerApplication()
        student1 = Student("John", "Doe", "john@doe.com")
        student2 = Student("Jane", "Spark", "jspark@gmail.com")
        tracker.students[student1.student_id] = student1
        tracker.students[student2.student_id] = student2
        assert tracker.validate_points_string(f"{student1.student_id} 1 2 3 4")
        assert tracker.validate_points_string(f"{student1.student_id} 0 0 0 0")
        assert tracker.validate_points_string(f"{student2.student_id} 1 2 3 4")

    def test_non_unique_email(self):
        tracker = TrackerApplication()
        student1 = Student("John", "Doe", "j@doe.com")
        tracker.students[student1.student_id] = student1
        assert tracker.is_email_taken("j@doe.com")
        assert tracker.validate_credentials(["Jane", "Doe", "j@doe.com"]) is None
class TestStudent():
    def test_student_id_increment(self):
        s1 = Student("John", "Doe", "john@doe.com")
        s2 = Student("Jane", "Doe", "jane@doe.com")
        assert s2.student_id == s1.student_id + 1
