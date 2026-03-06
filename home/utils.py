import json
from django_celery_beat.models import CrontabSchedule, PeriodicTask


def schedule_daily_task(
    name: str,
    task_path: str,
    hour: int,
    minute: int = 0,
    args: list | None = None,
    kwargs: dict | None = None,
    enabled: bool = True,
    timezone: str = "Asia/Qatar"
):
    """
    Create or update a daily scheduled celery task.

    Parameters
    ----------
    name : unique task identifier
    task_path : celery task path (example: "home.tasks.daily_report")
    hour : hour to run (0-23)
    minute : minute to run
    args : list of positional arguments
    kwargs : dict of keyword arguments
    enabled : enable/disable task
    timezone : schedule timezone
    """

    args = args or []
    kwargs = kwargs or {}

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=str(minute),
        hour=str(hour),
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
        timezone=timezone,
    )

    task, created = PeriodicTask.objects.update_or_create(
        name=name,
        defaults={
            "crontab": schedule,
            "task": task_path,
            "args": json.dumps(args),
            "kwargs": json.dumps(kwargs),
            "enabled": enabled,
        },
    )

    return task