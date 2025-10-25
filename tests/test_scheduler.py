import time
from datetime import datetime, timedelta

from promptclock.scheduler import PromptScheduler


def say_hi(name: str) -> None:
    """Simple function to simulate a scheduled job."""
    print(f"Hi {name}! Time is now {datetime.now().strftime('%H:%M:%S')}")


def test_schedule_adds_job() -> None:
    """Unit test that verifies PromptScheduler can run a scheduled job."""
    called: dict[str, tuple[str]] = {}

    def fake_func(prompt_id: str, text: str) -> None:
        called["ok"] = (prompt_id, text)

    sched = PromptScheduler()
    sched.start()

    run_time = datetime.now() + timedelta(seconds=2)
    sched.schedule_at("t1", run_time, fake_func, prompt_id="t1", text="hello")

    time.sleep(3)
    sched.shutdown()

    assert "ok" in called
    assert called["ok"] == ("t1", "hello")


if __name__ == "__main__":
    # Manual demo: run a real scheduled job for fun
    def say_hi_live(name: str) -> None:
        print(f"Hi {name}! Time is now {datetime.now().strftime('%H:%M:%S')}")

    sched = PromptScheduler()
    sched.start()

    run_time = datetime.now() + timedelta(seconds=5)
    sched.schedule_at("test-job", run_time, say_hi_live, name="Sai")

    print("Waiting 5 seconds...")
    time.sleep(8)
