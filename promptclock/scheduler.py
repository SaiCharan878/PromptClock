from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

logger = logging.getLogger("promptclock.scheduler")


class PromptScheduler:
    """Handles scheduling and running prompt jobs using APScheduler."""

    def __init__(self) -> None:
        """Initialize a background scheduler instance."""
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        """Start the scheduler."""
        logger.info("Scheduler started")
        self.scheduler.start()

    def shutdown(self) -> None:
        """Shutdown the scheduler gracefully."""
        logger.info("Scheduler shutting down")
        self.scheduler.shutdown(wait=False)

    def schedule_at(
        self,
        job_id: str,
        run_time: datetime,
        func: Callable[..., None],
        *args: object,
        **kwargs: object,
    ) -> None:
        """
        Schedule a function to run at a specific time.

        Args:
            job_id: Unique ID for the job.
            run_time: The datetime when the job should execute.
            func: The callable to execute.
            *args: Positional arguments for the callable.
            **kwargs: Keyword arguments for the callable.
        """
        try:
            trigger = DateTrigger(run_date=run_time)
            self.scheduler.add_job(func, trigger, id=job_id, args=args, kwargs=kwargs)
            logger.info("Job '%s' scheduled at %s", job_id, run_time.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            logger.exception("Failed to schedule job '%s': %s", job_id, e)
