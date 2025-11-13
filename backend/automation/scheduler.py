# backend/automation/scheduler.py
"""
XYLO — Automation Scheduler (Lightweight Version)

This module provides:
- A lightweight task scheduler (no external dependencies)
- Ability to run daily, weekly, and custom-timed jobs
- A unified registry for automation tasks
- Manual trigger support for the API backend
- Thread-safe loop for background execution

This is perfect for development and demo environments.
For production: replace with APScheduler / Celery / Redis workers.
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Dict, Any


# -------------------------------------------------------------------
# Task Registry
# -------------------------------------------------------------------

TASK_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_task(name: str, schedule: str, func: Callable):
    """
    Register a task with a cron-like schedule string:
    - "daily@22:00"
    - "weekly@mon@09:30"
    - "interval@300" - every 300 seconds
    """
    TASK_REGISTRY[name] = {
        "name": name,
        "schedule": schedule,
        "func": func,
        "last_run": None,
    }


# -------------------------------------------------------------------
# Schedule Parsing Helpers
# -------------------------------------------------------------------

def _should_run_daily(last_run: datetime, time_str: str) -> bool:
    now = datetime.now()
    # Convert "HH:MM"
    hh, mm = map(int, time_str.split(":"))
    target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)

    if last_run is None:
        return now >= target
    return last_run.date() < now.date() and now >= target


def _should_run_weekly(last_run: datetime, weekday: str, time_str: str) -> bool:
    now = datetime.now()
    weekday_map = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    target_day = weekday_map.index(weekday.lower())

    hh, mm = map(int, time_str.split(":"))
    target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)

    if now.weekday() != target_day:
        return False
    if last_run is None:
        return now >= target
    return last_run.isocalendar()[1] < now.isocalendar()[1] and now >= target


def _should_run_interval(last_run: datetime, seconds: int) -> bool:
    if last_run is None:
        return True
    return datetime.now() >= last_run + timedelta(seconds=seconds)


# -------------------------------------------------------------------
# Background Worker Thread
# -------------------------------------------------------------------

def _worker():
    while True:
        for name, task in TASK_REGISTRY.items():
            schedule = task["schedule"]
            func = task["func"]
            last = task["last_run"]

            try:
                if schedule.startswith("daily@"):
                    _, time_str = schedule.split("@")
                    if _should_run_daily(last, time_str):
                        print(f"[XYLO Scheduler] Running daily task: {name}")
                        func()
                        task["last_run"] = datetime.now()

                elif schedule.startswith("weekly@"):
                    _, weekday, time_str = schedule.split("@")
                    if _should_run_weekly(last, weekday, time_str):
                        print(f"[XYLO Scheduler] Running weekly task: {name}")
                        func()
                        task["last_run"] = datetime.now()

                elif schedule.startswith("interval@"):
                    _, seconds = schedule.split("@")
                    seconds = int(seconds)
                    if _should_run_interval(last, seconds):
                        print(f"[XYLO Scheduler] Running interval task: {name}")
                        func()
                        task["last_run"] = datetime.now()

            except Exception as e:
                print(f"[XYLO Scheduler] Error running task {name}: {e}")

        time.sleep(1)


# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------

def start_scheduler():
    """Start the automation engine in a background thread."""
    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    print("[XYLO Scheduler] Background scheduler started.")


def run_task_now(task_name: str):
    """Manually trigger a task (used by API backend)."""
    if task_name not in TASK_REGISTRY:
        raise ValueError(f"Task '{task_name}' not found.")
    func = TASK_REGISTRY[task_name]["func"]
    print(f"[XYLO Scheduler] Manually triggering: {task_name}")
    func()
    TASK_REGISTRY[task_name]["last_run"] = datetime.now()


# -------------------------------------------------------------------
# Example Default Tasks (Demo)
# -------------------------------------------------------------------

def daily_summary():
    print("[XYLO Automation] Generating daily financial summary (DEMO).")
    # In production:
    # summary = accounting_engine.daily_summary()
    # email_service.send(summary)
    pass


def weekly_backup():
    print("[XYLO Automation] Running weekly database backup (DEMO).")
    # Would run DB dump or upload to cloud storage here.
    pass


# Register demo tasks
register_task("daily_summary", "daily@22:00", daily_summary)
register_task("weekly_backup", "weekly@sun@03:00", weekly_backup)


# For local demo testing:
if __name__ == "__main__":
    start_scheduler()
    while True:
        time.sleep(10)
