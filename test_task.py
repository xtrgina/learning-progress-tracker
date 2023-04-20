# fmt: off
import pytest
from .task import TrackerApplication, Student


class TestTracker:
    @pytest.fixture(autouse=True)
    def setup_tracker(self):
        self.tracker = TrackerApplication()

    def test_correct_credentials(self):
        assert self.tracker.validate_credentials(["John", "Middle", "Smith", "email@dot.com"]) is not None
        assert self.tracker.validate_credentials(["John", "Smith", "email@dot.com"]) is not None

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

class TestStudent():
    def test_student_id_increment(self):
        s1 = Student("John", "Doe", "john@doe.com")
        s2 = Student("Jane", "Doe", "jane@doe.com")
        assert s2.student_id == s1.student_id + 1
