"""
Task manager
Organize, manage, and prioritize tasks.
"""
import copy


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
        """Print the details of all tasks."""
        for task in self.tasks:
            task.print_details()

    def chunk_tasks(self, minimum_time=1):
        """Chunk the tasks into shorter durations."""
        for task in self.tasks:
            while task.hours > 2 * minimum_time:
                new_task = copy.copy(task)
                new_task.hours = minimum_time
                self.tasks.append(new_task)
                task.hours -= minimum_time


my_task = Task("code", "6/15/2020", 8)
my_second_task = Task("eat", "6/16/2020", 16)
my_schedule = Schedule([my_task, my_second_task])
my_schedule.chunk_tasks(0.75)
my_schedule.print_details()
