import sys
import re
from dataclasses import dataclass, field
from itertools import count
from statistics import fmean


@dataclass
class Student:
    first_name: str
    last_name: str
    email: str
    student_id: int = field(default_factory=count(1000).__next__)


@dataclass
class Course:
    name: str
    pass_requirement: int
    student_records: dict[int, int] = field(default_factory=dict)
    submissions: list[int] = field(default_factory=list)

    def update_student_record(self, student_id: int, points: int) -> None:
        if points == 0:
            return
        if student_id in self.student_records:
            self.student_records[student_id] += points
        else:
            self.student_records[student_id] = points
        self.submissions.append(points)

    def get_student_progress(self) -> list:
        student_progress = []
        for student_id, points in self.student_records.items():
            completed_percentage = f"{(points / self.pass_requirement) * 100:.1f}%"
            student_progress.append((student_id, points, completed_percentage))
        return student_progress

    def average_points_per_submission(self) -> float:
        if not self.submissions:
            return 0
        return fmean(self.submissions)

    def total_number_of_submissions(self) -> int:
        return len(self.submissions)

    def points_by_student(self, student_id: int) -> int:
        if student_id not in self.student_records:
            return 0
        return self.student_records[student_id]

    def enrolled_count(self) -> int:
        return len(self.student_records)


class TrackerApplication:
    def __init__(self):
        self.students = {}
        self.courses = {
            "python": Course("Python", 600),
            "dsa": Course("DSA", 400),
            "databases": Course("Databases", 480),
            "flask": Course("Flask", 550),
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
                case "find":
                    self.find_student()
                case "list":
                    self.list_students()
                case "statistics":
                    self.statistics()
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
                print("Incorrect points format")
                continue
            student_id, points = validated_input
            for index, course_name in enumerate(self.courses):
                self.update_course_record(course_name, student_id, points[index])
            print("Points updated")

    def validate_points_string(self, user_input):
        input_fields = user_input.split()
        if len(input_fields) != 5:
            return None
        student_id = self.validate_student_id(input_fields[0])
        if student_id is None:
            return None
        try:
            points = [int(x) for x in input_fields[1:5]]
        except ValueError:
            return None
        for number in points:
            if number < 0:
                return None
        return student_id, points

    def validate_student_id(self, input_id):
        try:
            student_id = int(input_id)
        except ValueError:
            print(f"No student is found for id={input_id}")
            return None
        if student_id not in self.students:
            print(f"No student is found for id={input_id}")
            return None
        return student_id

    def update_course_record(self, course_name, student_id, points):
        course = self.courses[course_name]
        course.update_student_record(student_id, points)

    def find_student(self):
        print("Enter an id or 'back' to return: ")
        while (user_input := input()) != "back":
            student_id = self.validate_student_id(user_input)
            if student_id is None:
                continue
            course_info = []
            for course_name, course in self.courses.items():
                points = course.points_by_student(student_id)
                course_info.append(f"{course_name}={points}")
            print(f"{student_id} points: {'; '.join(course_info)}")

    def statistics(self):
        most_popular, least_popular = self.most_and_least_popular_courses()
        most_active, least_active = self.most_and_least_active_courses()
        easiest, hardest = self.easiest_and_hardest_courses()
        print("Type the name of a course to see details or 'back' to quit:")
        print(f"Most popular: {most_popular}")
        print(f"Least popular: {least_popular}")
        print(f"Highest activity: {most_active}")
        print(f"Lowest activity: {least_active}")
        print(f"Easiest course: {easiest}")
        print(f"Hardest course: {hardest}")
        while (course_name := input().lower().strip()) != "back":
            if course_name not in self.courses:
                print("Unknown course")
                continue
            self.display_course_statistics(course_name)

    def most_and_least_popular_courses(self):
        courses = list(self.courses.values())
        courses.sort(key=lambda x: x.enrolled_count(), reverse=True)

        highest = courses[0].enrolled_count()
        lowest = courses[-1].enrolled_count()
        most_popular = [
            course.name for course in courses if course.enrolled_count() == highest
        ]
        least_popular = [
            course.name
            for course in courses
            if course.enrolled_count() == lowest and course.name not in most_popular
        ]

        if highest == 0:
            return "n/a", "n/a"
        if not least_popular:
            return ", ".join(most_popular), "n/a"

        return ", ".join(most_popular), ", ".join(least_popular)

    def most_and_least_active_courses(self):
        courses = list(self.courses.values())
        courses.sort(key=lambda x: x.total_number_of_submissions(), reverse=True)
        highest = courses[0].total_number_of_submissions()
        lowest = courses[-1].total_number_of_submissions()
        most_active = [
            course.name
            for course in courses
            if course.total_number_of_submissions() == highest
        ]
        least_active = [
            course.name
            for course in courses
            if course.total_number_of_submissions() == lowest
            and course.name not in most_active
        ]

        if highest == 0:
            return "n/a", "n/a"
        if not least_active:
            return ", ".join(most_active), "n/a"

        return ", ".join(most_active), ", ".join(least_active)

    def easiest_and_hardest_courses(self):
        courses = list(self.courses.values())
        courses.sort(key=lambda x: x.average_points_per_submission(), reverse=True)
        highest = courses[0].average_points_per_submission()
        lowest = courses[-1].average_points_per_submission()
        easiest = [
            course.name
            for course in courses
            if course.average_points_per_submission() == highest
        ]
        hardest = [
            course.name
            for course in courses
            if course.average_points_per_submission() == lowest
            and course.name not in easiest
        ]

        if highest == 0:
            return "n/a", "n/a"
        if not hardest:
            return ", ".join(easiest), "n/a"

        return ", ".join(easiest), ", ".join(hardest)

    def display_course_statistics(self, course_name):
        course = self.courses[course_name]
        print(course.name)
        print(f"{'id':<8}{'points':<10}completed")
        student_statistics = sorted(
            course.get_student_progress(),
            key=lambda data: (data[1], -data[0]),
            reverse=True,
        )
        for student_id, points, completed in student_statistics:
            print(f"{student_id:<8d}{points:<10d}{completed}")


if __name__ == "__main__":
    tracker = TrackerApplication()
    tracker.execute()
