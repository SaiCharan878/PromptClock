from __future__ import annotations

import logging
import signal
import sys
import time
from typing import Any

from promptclock.logging_setup import setup_logging
from promptclock.scheduler import PromptScheduler
from promptclock.storage import load_prompts
from promptclock.typer import type_and_send
from promptclock.window import focus_comet

logger = logging.getLogger("promptclock.main")


def run_job(prompt_id: str, text: str) -> None:
    """Callback executed when a scheduled prompt runs."""
    try:
        logger.info("Running job %s: %s", prompt_id, text)
        if not focus_comet():
            logger.error("Failed to focus Comet window; skipping prompt.")
            return
        time.sleep(0.5)
        type_and_send(text)
        logger.info("Prompt '%s' executed successfully.", prompt_id)
    except Exception as e:
        logger.exception("Error while running job %s: %s", prompt_id, e)


def signal_handler(sig: int, frame: Any) -> None:
    """Handle Ctrl+C or SIGINT to shut down gracefully."""
    logger.info("Interrupt received (signal %s). Shutting down...", sig)
    sys.exit(0)


def main() -> None:
    """Main entry point to start PromptClock."""
    setup_logging()
    logger.info("PromptClock starting...")

    signal.signal(signal.SIGINT, signal_handler)

    prompts = load_prompts()
    if not prompts:
        logger.warning("No prompts found to schedule.")
        return

    scheduler = PromptScheduler()
    scheduler.start()

    for p in prompts:
        scheduler.schedule_at(
            job_id=p.id,
            run_time=p.run_time,
            func=run_job,
            prompt_id=p.id,
            text=p.text,
        )

    logger.info("Scheduled %d prompt(s).", len(prompts))
    logger.info("PromptClock is running. Keep this window open.")
    logger.info("Move mouse to top-left corner anytime to abort typing safely.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("PromptClock stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
