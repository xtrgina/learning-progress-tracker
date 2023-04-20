import sys
import re
from dataclasses import dataclass


@dataclass
class Student:
    first_name: str
    last_name: str
    email: str


class TrackerApplication:
    def __init__(self):
        self.students = {}

    def execute(self):
        print("Learning progress tracker")
        while (command := input().strip()) != "exit":
            if not command:
                print("No input")
                continue
            match command:
                case "add students":
                    self.add_students()
                case "back":
                    print("Enter 'exit' to exit the program")
                case _:
                    print("Unknown command!")
        print("Bye!")
        sys.exit()

    def add_students(self):
        students_added = 0
        print("Enter student credentials or 'back' to return: ")
        while (user_input := input()) != "back":
            if (credentials := self.validate_credentials(user_input.split())) is None:
                continue
            first_name, last_name, email = credentials
            student = Student(first_name, last_name, email)
            self.students[email] = student
            print("The student has been added")
            students_added += 1
        print(
            f"Total {students_added} student{'' if students_added == 1 else 's'} have been added"
        )

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


def main():
    tracker = TrackerApplication()
    tracker.execute()


if __name__ == "__main__":
    main()
