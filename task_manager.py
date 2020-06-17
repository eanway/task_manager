"""
Task manager
Organize, manage, and prioritize tasks.
"""
import datetime


class TaskTriage(object):
    """
    An assessment of a task.
    """

    def __init__(self, name, hours_needed, remaining_hours):
        self.name = name
        self.hours_needed = hours_needed
        self.remaining_hours = remaining_hours
        self.possible = 0 < hours_needed < remaining_hours
        if self.possible:
            self.priority = hours_needed / remaining_hours
        else:
            self.priority = 0


class Task(object):
    """
    A task that needs to be completed by a due date.
    """

    version = "0.1"

    def __init__(self, name, due_date, hours):
        self.name = name
        self.due_date = datetime.datetime.strptime(due_date, "%m/%d/%Y").date()
        self.hours = hours
        self.priority = 0
        self.triage_report = None

    def print_details(self):
        """Print the details of the task."""
        print(
            "Task {} is due on {} and will take {} hours".format(
                self.name,
                self.due_date,
                self.hours
            )
        )

    def triage(self, current_date, day_length, current_hour):
        """Determine the task priority."""
        remaining_hours = ((self.due_date - current_date).days + 1) * day_length - current_hour
        self.triage_report = TaskTriage(self.name, self.hours, remaining_hours)


class TodoListTriage(object):
    """
    An assessment of the current list of tasks.
    """

    def __init__(self, todo_list, current_date, day_length, current_hour):
        self.hours_needed = 0
        self.remaining_hours = 0
        self.triage_reports = []
        for task in todo_list:
            task.triage(current_date, day_length, current_hour)
            if not task.triage_report.possible:
                todo_list.remove(task)
            else:
                self.triage_reports.append(task.triage_report)
                self.hours_needed += task.triage_report.hours_needed
                self.remaining_hours += task.triage_report.remaining_hours
        if self.remaining_hours > 0:
            self.average_priority = self.hours_needed / self.remaining_hours
        else:
            self.average_priority = 0

    def top_priority(self):
        """Get the highest priority."""
        if not self.triage_reports:
            return 0
        else:
            return max(triage_report.priority for triage_report in self.triage_reports)


class TodoList(object):
    """
    A list of tasks.
    """

    version = "0.1"

    def __init__(self, tasks=None):
        if tasks is None:
            tasks = []
        self.tasks = tasks
        self.triage_report = None

    def print_details(self):
        """Print the details of all tasks."""
        for task in self.tasks:
            task.print_details()

    def min_date(self):
        """Get the minimum due date from all tasks."""
        return min(task.due_date for task in self.tasks)

    def triage(self, current_date, day_length, current_hour):
        """Set the priority level of all tasks."""
        self.triage_report = TodoListTriage(self.tasks, current_date, day_length, current_hour)

    def top_priority(self):
        """Get the task with the highest priority."""
        if not self.tasks:
            return None
        else:
            return max(self.tasks, key=lambda task: task.triage_report.priority)


class Event(object):
    """
    An event on one day.
    """

    def __init__(self, task_name, start_time, end_time, triage_report):
        self.task_name = task_name
        self.start_time = start_time
        self.end_time = end_time
        self.triage_report = triage_report


class DailyPlan(object):
    """
    A plan of events for one day.
    """

    def __init__(self, date):
        self.date = date
        self.events = []

    def add_event(self, task_name, start_time, end_time, triage_report=None):
        self.events.append(Event(task_name, start_time, end_time, triage_report))


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
            top_task = None
            while hours_remaining > 0:
                todo_list.triage(current_date, day_length, current_hour)
                top_task = todo_list.top_priority()
                if top_task is None:
                    break
                my_day.add_event(
                    top_task.name,
                    current_hour,
                    current_hour + minimum_hours,
                    todo_list.triage_report
                )
                current_hour += minimum_hours
                hours_remaining -= minimum_hours
                top_task.hours -= minimum_hours
            if top_task is None:
                break
            self.schedule.append(my_day)
            current_date += datetime.timedelta(days=1)

    def print_schedule(self):
        """Print the input todo_list"""
        for day in self.schedule:
            print(day.date)
            for event in day.events:
                triage_report = event.triage_report
                print("{} - {}: {} (top: {}, average: {})".format(
                    event.start_time,
                    event.end_time,
                    event.task_name,
                    round(triage_report.top_priority(), 2),
                    round(triage_report.average_priority, 2)
                ))


my_task = Task("code", "6/15/2020", 6)
my_second_task = Task("eat", "6/16/2020", 10)
my_third_task = Task("sleep", "6/16/2020", 8)
my_todo = TodoList([my_task, my_second_task, my_third_task])
my_schedule = Schedule(my_todo, start_date="6/14/2020")
my_schedule.print_schedule()
