"""
Task manager
Organize, manage, and prioritize tasks.
"""
import datetime


def create_task(name, due_date, hours):
    """
    A task that needs to be completed by a due date.
    """
    return {
        "name": name,
        "due_date": datetime.datetime.strptime(due_date, "%m/%d/%Y").date(),
        "hours": hours
    }


def create_event(task_name, start_time, end_time, triage_report):
    """
    A planned event occurring during the day.
    """
    return {
        "task_name": task_name,
        "start_time": start_time,
        "end_time": end_time,
        "triage_report": triage_report
    }


def create_daily_plan(date, events=None):
    """
    A plan of events for one day.
    """
    if events is None:
        events = []
    return {
        "date": date,
        "events": events
    }


def create_triage_report(name, hours_needed, hours_remaining):
    """
    A report of whether a task is possible.
    """
    possible = 0 <= hours_needed < hours_remaining
    if possible:
        priority = hours_needed / hours_remaining
    else:
        priority = 0
    return {
        "name": name,
        "hours_needed": hours_needed,
        "hours_remaining": hours_remaining,
        "possible": possible,
        "priority": priority
    }


def triage_task(task, current_date, day_length, current_hour):
    """
    Determine the task priority.
    """
    hours_remaining = ((task["due_date"] - current_date).days + 1) * day_length - current_hour
    hours_needed = task["hours"]
    return create_triage_report(task["name"], hours_needed, hours_remaining)


def triage_todo_list(todo_list, current_date, day_length, current_hour):
    """
    Determine the priority for every task on a list.
    """
    hours_needed = 0
    hours_remaining = 0
    triage_reports = []
    for task in todo_list:
        task_triage_report = triage_task(task, current_date, day_length, current_hour)
        if not task_triage_report["possible"]:
            todo_list.remove(task)
        else:
            triage_reports.append(task_triage_report)
        hours_needed += task_triage_report["hours_needed"]
        hours_remaining += task_triage_report["hours_remaining"]
    return {
        "triage": create_triage_report("total", hours_needed, hours_remaining),
        "triage_reports": triage_reports,
        "top_priority": None
    }


def create_schedule(todo_list, start_date=None, minimum_hours=1.0, day_length=8.0):
    """
    A schedule of tasks to complete over multiple days.
    """
    if start_date is None:
        current_date = min(task.due_date for task in todo_list)
    else:
        current_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
    schedule = []
    while todo_list:
        my_daily_plan = create_daily_plan(current_date)
        current_hour = 0
        hours_remaining = day_length
        top_task = None
        while hours_remaining > 0:
            todo_list_triage_report = triage_todo_list(todo_list, current_date, day_length, current_hour)
            if not todo_list:
                top_task = None
                break
            current_top_triage_report = max(
                todo_list_triage_report["triage_reports"],
                key=lambda report: report["priority"]
            )
            todo_list_triage_report["top_priority"] = current_top_triage_report
            top_task = [task for task in todo_list if task["name"] == current_top_triage_report["name"]].pop()
            my_event = create_event(
                top_task["name"],
                current_hour,
                current_hour + minimum_hours,
                todo_list_triage_report
            )
            my_daily_plan["events"].append(my_event)
            current_hour += minimum_hours
            hours_remaining -= minimum_hours
            top_task["hours"] -= minimum_hours
        if top_task is None:
            break
        schedule.append(my_daily_plan)
        current_date += datetime.timedelta(days=1)
    return schedule


my_task = create_task("code", "6/15/2020", 6)
my_second_task = create_task("eat", "6/16/2020", 10)
my_third_task = create_task("sleep", "6/16/2020", 8)
my_todo = [my_task, my_second_task, my_third_task]
my_schedule = create_schedule(my_todo, start_date="6/14/2020")
for day in my_schedule:
    print(day["date"])
    for event in day["events"]:
        todo_triage_report = event["triage_report"]
        top_triage_report = todo_triage_report["top_priority"]
        print("{}-{}: {} ({})".format(
            event["start_time"],
            event["end_time"],
            event["task_name"],
            round(top_triage_report["priority"], 2)
        ))
