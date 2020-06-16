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


my_task = Task("code", "6/15/2020", 8)
my_second_task = Task("eat", "6/16/2020", 16)
schedule = [my_task, my_second_task]
for task in schedule:
    task.print_details()
