import sys
import re
from dataclasses import dataclass, field
from itertools import count


@dataclass
class Student:
    first_name: str
    last_name: str
    email: str
    student_id: int = field(default_factory=count(10000).__next__)


@dataclass
class Course:
    name: str
    student_records: dict[int, int] = field(default_factory=dict)

    def update_student_record(self, student_id: int, points: int) -> None:
        if student_id in self.student_records:
            self.student_records[student_id] += points
        else:
            self.student_records[student_id] = points


class TrackerApplication:
    def __init__(self):
        self.students = {}
        self.courses = {
            "Python": Course("Python"),
            "DSA": Course("DSA"),
            "Databases": Course("Databases"),
            "Flask": Course("Flask"),
        }

    def execute(self):
        print("Learning progress tracker")
        while (command := input().strip()) != "exit":
            if not command:
                print("No input")
                continue
            match command:
                case "add students":
                    self.add_students()
                case "add points":
                    self.add_points()
                case "back":
                    print("Enter 'exit' to exit the program")
                case "list":
                    self.list_students()
                case _:
                    print("Unknown command!")
        print("Bye!")
        sys.exit()

    def add_students(self):
        students_added = 0
        print("Enter student credentials or 'back' to return: ")
        while (user_input := input()) != "back":
            credentials = self.validate_credentials(user_input.split())
            if credentials is None:
                continue
            first_name, last_name, email = credentials
            student = Student(first_name, last_name, email)
            self.students[student.student_id] = student
            print("The student has been added")
            students_added += 1
        print(
            f"Total {students_added} student{'' if students_added == 1 else 's'} have been added"
        )

    def is_email_taken(self, email):
        for student in self.students.values():
            if student.email == email:
                return True
        return False

    def validate_credentials(self, credentials):
        if len(credentials) < 3:
            print("Incorrect credentials")
            return None
        first_name = credentials[0]
        last_name = " ".join(credentials[1:-1])
        email = credentials[-1]
        if not self.validate_name(first_name):
            print("Incorrect first name")
            return None
        if not self.validate_name(last_name):
            print("Incorrect last name")
            return None
        if not self.validate_email(email):
            print("Incorrect email")
            return None
        if self.is_email_taken(email):
            print("This email is already taken")
            return None
        return first_name, last_name, email

    @staticmethod
    def validate_name(name):
        pattern = re.compile("^[a-zA-Z]['-]?([a-zA-Z]+['-]?)*[a-zA-Z]$")
        if len(name) == 1:
            return pattern.match(name)
        for part in name.split():
            if not pattern.match(part):
                return False
        return True

    @staticmethod
    def validate_email(email):
        pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        return pattern.match(email)

    def list_students(self):
        if not self.students:
            print("No students found")
        print("Students:")
        for student_id in self.students:
            print(student_id)

    def add_points(self):
        print("Enter an id and points or 'back' to return")
        while (user_input := input()) != "back":
            validated_input = self.validate_points_string(user_input)
            if validated_input is None:
                continue
            student_id, points = validated_input
            for index, course_name in enumerate(self.courses):
                self.update_course_record(course_name, student_id, points[index])
            print("Points updated")

    def validate_points_string(self, user_input):
        input_fields = user_input.split()
        if len(input_fields) != 5:
            print("Incorrect points format")
            return None
        try:
            student_id = int(input_fields[0])
        except ValueError:
            print(f"No student is found for id={input_fields[0]}")
            return None
        try:
            points = [int(x) for x in input_fields[1:5]]
        except ValueError:
            print("Incorrect points format")
            return None
        if student_id not in self.students:
            print(f"No student is found for id={student_id}")
            return None
        for number in points:
            if number < 0:
                print("Incorrect points format")
                return None
        return student_id, points

    def update_course_record(self, course_name, student_id, points):
        course = self.courses[course_name]
        course.update_student_record(student_id, points)


if __name__ == "__main__":
    tracker = TrackerApplication()
    tracker.execute()
