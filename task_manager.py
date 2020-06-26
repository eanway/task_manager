"""
Task manager
Organize, manage, and prioritize tasks.
"""
from datetime import datetime, date, timedelta


class TaskManager():
    """
    Create, edit, and schedule tasks
    """

    def __init__(self):
        self.task_list = []
        self.schedule = []
    
    def add_task(self, name, due_date, hours):
        """
        a task that needs to be completed by a due date.
        """
        self.task_list.append({
            "name": name,
            "due_date": datetime.strptime(due_date, "%m/%d/%Y").date(),
            "hours": hours
        }) 

    def create_schedule(self, start_date=None, minimum_hours=1.0, day_length=8.0):
        """
        A schedule of tasks to complete over multiple days.
        """
        todo_list = self.task_list.copy()
        if start_date is None:
            current_date = date.today()
        else:
            current_date = datetime.strptime(start_date, "%m/%d/%Y").date()
        schedule = []
        time_from_start = 0
        while todo_list:
            my_daily_plan = self.create_daily_plan(current_date)
            current_hour = 0
            hours_remaining = day_length
            top_task = None
            while hours_remaining > 0:
                todo_list_triage_report = self.triage_todo_list(todo_list, current_date, day_length, current_hour)
                if not todo_list:
                    top_task = None
                    break
                current_top_triage_report = max(
                    todo_list_triage_report["triage_reports"],
                    key=lambda report: report["priority"]
                )
                todo_list_triage_report["top_priority"] = current_top_triage_report
                top_task = [task for task in todo_list if task["name"] == current_top_triage_report["name"]].pop()
                my_event = self.create_event(
                    top_task["name"],
                    time_from_start,
                    current_hour,
                    current_hour + minimum_hours,
                    todo_list_triage_report
                )
                my_daily_plan["events"].append(my_event)
                current_hour += minimum_hours
                time_from_start += minimum_hours
                hours_remaining -= minimum_hours
                top_task["hours"] -= minimum_hours
            if top_task is None:
                break
            schedule.append(my_daily_plan)
            current_date += timedelta(days=1)
        return schedule


    def create_event(self, task_name, time_from_start, start_time, end_time, triage_report):
        """
        a planned event occurring during the day.
        """
        return {
            "task_name": task_name,
            "time_from_start": time_from_start,
            "start_time": start_time,
            "end_time": end_time,
            "triage_report": triage_report
        }


    def create_daily_plan(self, date, events=None):
        """
        a plan of events for one day.
        """
        if events is None:
            events = []
        return {
            "date": date,
            "events": events
        }


    def create_triage_report(self, name, hours_needed, hours_remaining):
        """
        a report of whether a task is possible.
        """
        possible = 0 < hours_needed <= hours_remaining
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


    def triage_task(self, task, current_date, day_length, current_hour):
        """
        determine the task priority.
        """
        hours_remaining = ((task["due_date"] - current_date).days + 1) * day_length - current_hour
        hours_needed = task["hours"]
        return self.create_triage_report(task["name"], hours_needed, hours_remaining)


    def triage_todo_list(self, todo_list, current_date, day_length, current_hour):
        """
        determine the priority for every task on a list.
        """
        hours_needed = 0
        hours_remaining = 0
        triage_reports = []
        for task in todo_list[:]:
            task_triage_report = self.triage_task(task, current_date, day_length, current_hour)
            if not task_triage_report["possible"]:
                todo_list.remove(task)
            else:
                triage_reports.append(task_triage_report)
            hours_needed += task_triage_report["hours_needed"]
            hours_remaining += task_triage_report["hours_remaining"]
        return {
            "triage": self.create_triage_report("total", hours_needed, hours_remaining),
            "triage_reports": triage_reports,
            "top_priority": None
        }

    def print_schedule(self):
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

    def get_schedule_table(self):
        list_main = []
        for day in self.schedule:
            date = day["date"]
            for event in day["events"]:
                time_from_start = event["time_from_start"]
                start_time = event["start_time"]
                end_time = event["end_time"]
                for report in event["triage_report"]["triage_reports"]:
                    task_report_triage_name = report["name"]
                    task_report_triage_hours_needed = report["hours_needed"]
                    task_report_triage_hours_remaining = report["hours_remaining"]
                    task_report_triage_possible = report["possible"]
                    task_report_triage_priority = report["priority"]
                    row_information = {
                        "date": date,
                        "time_from_start": time_from_start,
                        "start_time": start_time,
                        "end_time": end_time,
                        "task_name": task_report_triage_name,
                        "task_hours_needed": task_report_triage_hours_needed,
                        "task_hours_remaining": task_report_triage_hours_remaining,
                        "task_possible": task_report_triage_possible,
                        "task_priority": task_report_triage_priority
                    }
                    list_main.append(row_information)
        return list_main

if __name__ == "__main__":
    my_TaskManager = TaskManager()
    my_TaskManager.add_task("code", "7/15/2020", 16)
    my_TaskManager.add_task("eat", "7/16/2020", 8)
    my_TaskManager.add_task("sleep", "7/17/2020", 16)
    my_TaskManager.create_schedule(start_date="6/12/2020")
    list_main = my_TaskManager.get_schedule_table()
	
    import pandas as pd
    df_main = pd.DataFrame(list_main)
    print(df_main.head())
    df_main.set_index("time_from_start", inplace=True)

    import matplotlib.pyplot as plt
    df_main.groupby("task_name")["task_priority"].plot(legend=True)
    plt.show()
