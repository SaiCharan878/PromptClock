import logging
import time

import pygetwindow as gw
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from .config import settings

logger = logging.getLogger("promptclock.window")


class FocusError(Exception):
    pass


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    retry=retry_if_exception_type(FocusError),
    reraise=True,
)
def focus_comet() -> bool:
    """Bring Comet to front with up to 3 retries."""
    matches = [t for t in gw.getAllTitles() if settings.window_title.lower() in t.lower()]
    if not matches:
        logger.warning("No window found containing '%s'", settings.window_title)
        raise FocusError("Window not found")

    title = matches[0]
    try:
        w = gw.getWindowsWithTitle(title)[0]
        w.activate()
        time.sleep(settings.post_focus_delay)
        logger.info("Focused window via pygetwindow: '%s'", title)
        return True
    except Exception as e:
        logger.debug("pygetwindow failed: %s", e)

    # Fallback
    try:
        from pywinauto import Application

        app = Application().connect(title_re=title)
        window = app.window(title_re=title)
        window.set_focus()
        window.set_foreground()
        time.sleep(settings.post_focus_delay)
        logger.info("Focused window via pywinauto: '%s'", title)
        return True
    except Exception as e2:
        logger.error("pywinauto failed: %s", e2)
        raise FocusError(str(e2)) from e2
