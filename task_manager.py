"""
Task manager
Organize, manage, and prioritize tasks.
"""
import math

import numpy

import datetime


class Task(object):
    """
    A task that needs to be completed by a due date.
    """

    version = "0.1"

    def __init__(self, name, due_date, hours):
        self.name = name
        self.due_date = datetime.datetime.strptime(due_date, "%m/%d/%Y").date()
        self.hours = hours
        self.stress = 0

    def print_details(self):
        """Print the details of the task."""
        print(
            "Task {} is due on {} and will take {} hours".format(
                self.name,
                self.due_date,
                self.hours
            )
        )


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

    def set_priorities(self, current_date, day_length, current_hour):
        for task in self.tasks:
            if task.hours <= 0 or current_date > task.due_date:
                self.tasks.remove(task)
                break
            task.stress = task.hours / (((task.due_date - current_date).days + 1) * day_length - current_hour)

    def top_priority(self, current_date, day_length, current_hour):
        self.set_priorities(current_date, day_length, current_hour)
        if not self.tasks:
            return None
        else:
            return max(self.tasks, key=lambda task: task.stress)


class Event(object):
    """
    An event on one day.
    """

    def __init__(self, task_name, start_time, end_time):
        self.task_name = task_name
        self.start_time = start_time
        self.end_time = end_time


class DailyPlan(object):
    """
    A plan of events for one day.
    """

    def __init__(self, date):
        self.date = date
        self.events = []

    def add_event(self, task_name, start_time, end_time):
        self.events.append(Event(task_name, start_time, end_time))


class Schedule(object):
    """
    A schedule of tasks to complete over multiple days.
    """

    def __init__(self, todo_list, start_date=None, minimum_hours=1.0, day_length=8.0):
        if start_date is None:
            current_date = todo_list.min_date()
        else:
            current_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
        self.schedule = []
        while todo_list.tasks:
            my_day = DailyPlan(current_date)
            current_hour = 0
            hours_remaining = day_length
            while hours_remaining > 0:
                top_task = todo_list.top_priority(current_date, day_length, current_hour)
                if top_task is None:
                    break
                my_day.add_event(top_task.name, current_hour, current_hour + minimum_hours)
                current_hour += minimum_hours
                hours_remaining -= minimum_hours
                top_task.hours -= minimum_hours
            self.schedule.append(my_day)
            current_date += datetime.timedelta(days=1)

    def print_schedule(self):
        """Print the input todo_list"""
        for day in self.schedule:
            print(day.date)
            for event in day.events:
                print("{} - {}: {}".format(event.start_time, event.end_time, event.task_name))


my_task = Task("code", "6/15/2020", 8)
my_second_task = Task("eat", "6/16/2020", 16)
my_todo = TodoList([my_task, my_second_task])
my_schedule = Schedule(my_todo, start_date="6/14/2020")
my_schedule.print_schedule()
