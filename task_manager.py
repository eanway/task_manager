"""
Task manager
Organize, manage, and prioritize tasks.
"""
import math

import numpy


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

    def chunk_hours(self, minimum_hours=1.0):
        """Chunk the task hours into blocks with a minimum size."""
        if isinstance(self.hours, list):
            self.sum_hours()

        number_of_chunks = math.floor(self.hours / minimum_hours)
        remainder = self.hours % minimum_hours
        chunks = [minimum_hours] * number_of_chunks
        chunks[-1] += remainder
        self.hours = chunks

    def sum_hours(self):
        """Sum the chunks of time into a single value."""
        self.hours = sum(self.hours)


class TodoList(object):
    """
    A list of tasks.
    """

    version = "0.1"

    def __init__(self, tasks=None):
        if tasks is None:
            tasks = []
        self.tasks = tasks

    def print_details(self):
        """Print the details of all tasks."""
        for task in self.tasks:
            task.print_details()

    def min_date(self):
        return min(task.due_date for task in self.tasks)


class Schedule(object):
    """
    A schedule of tasks to complete.
    """

    def __init__(self, todo_list, start_date=None, minimum_hours=1.0, day_length=8.0):
        self.todo_list = todo_list
        if start_date is None:
            start_date = self.todo_list.min_date()
        self.start_date = start_date
        self.time_blocks = numpy.arange(0, day_length, minimum_hours)

    def print_todo(self):
        """Print the input todo_list"""
        self.todo_list.print_details()

    def chunk_tasks(self, minimum_time=1.0):
        """Chunk the tasks into shorter durations."""
        for task in self.tasks:
            task.chunk_hours(minimum_time)

    def sum_tasks(self):
        """Sum each task duration into a single value."""
        for task in self.tasks:
            task.sum_hours()


my_task = Task("code", "6/15/2020", 8)
my_second_task = Task("eat", "6/16/2020", 16)
my_todo = TodoList([my_task, my_second_task])
my_schedule = Schedule(my_todo)
my_schedule.print_todo()
print(my_schedule.start_date)
