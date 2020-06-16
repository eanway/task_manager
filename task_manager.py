"""
Task manager
Organize, manage, and prioritize tasks.
"""


class Task(object):
    """
    A task that needs to be completed by a due date.
    """

    version = "0.1"

    def __init__(self, name, due_date, hours):
        self.name = name
        self.due_date = due_date
        self.hours = hours

    def print_details(self):
        """Print the details of the task."""
        print(
            "Task {} is due on {} and will take {} hours".format(
                self.name,
                self.due_date,
                self.hours
            )
        )

class Schedule(object):
    """
    A list of tasks.
    """

    version = "0.1"

    def __init__(self, tasks=[]):
        self.tasks = tasks

    def print_details(self):
        for task in self.tasks:
            task.print_details()

my_task = Task("code", "6/15/2020", 8)
my_second_task = Task("eat", "6/16/2020", 16)
my_schedule = Schedule([my_task, my_second_task])
my_schedule.print_details()
