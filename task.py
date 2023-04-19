import sys


class TrackerApplication:
    def __init__(self):
        pass

    def execute(self):
        print("Learning progress tracker")
        while (command := input().strip()) != "exit":
            if not command:
                print("No input")
            else:
                print("Unknown command!")
        print("Bye!")


def main():
    tracker = TrackerApplication()
    tracker.execute()


if __name__ == "__main__":
    main()
