import logging
import time

import pyautogui
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from .config import settings

logger = logging.getLogger("promptclock.typer")


class TypingError(Exception):
    pass


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    retry=retry_if_exception_type(TypingError),
    reraise=True,
)
def type_and_send(text: str) -> None:
    """Type text with up to 3 retries."""
    try:
        if settings.click_xy:
            x, y = settings.click_xy
            pyautogui.click(x=x, y=y)
            time.sleep(0.2)

        logger.info("Typing %d characters...", len(text))
        pyautogui.typewrite(text, interval=settings.typing_delay)
        pyautogui.press("enter")
        logger.info("Message sent")
    except Exception as e:
        logger.warning("Typing attempt failed: %s", e)
        raise TypingError(str(e)) from e
