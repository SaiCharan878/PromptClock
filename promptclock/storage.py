from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from dateutil import parser as dtparse
from pydantic import BaseModel

logger = logging.getLogger("promptclock.storage")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "prompts.json"


class ScheduledPrompt(BaseModel):
    """Model representing a single scheduled prompt."""

    id: str
    text: str
    run_time: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ScheduledPrompt:
        """Create a ScheduledPrompt object from a dictionary."""
        try:
            run_time = (
                data["run_time"]
                if isinstance(data["run_time"], datetime)
                else dtparse.parse(data["run_time"])
            )
            return cls(id=data["id"], text=data["text"], run_time=run_time)
        except Exception as e:
            logger.exception("Error parsing prompt data: %s", e)
            raise


def load_prompts() -> list[ScheduledPrompt]:
    """Load scheduled prompts from a JSON file."""
    try:
        if not DATA_PATH.exists():
            logger.warning("Prompts file not found at %s", DATA_PATH)
            return []

        with open(DATA_PATH) as f:
            raw_data: list[dict[str, Any]] = json.load(f)

        prompts = [ScheduledPrompt.from_dict(item) for item in raw_data]
        logger.info("Loaded %d prompt(s) from %s", len(prompts), DATA_PATH)
        return prompts

    except Exception as e:
        logger.exception("Failed to load prompts: %s", e)
        return []
