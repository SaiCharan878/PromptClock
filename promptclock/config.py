"""
Configuration for PromptClock using Pydantic Settings.
Provides typed, validated access to environment variables (.env file).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Window & Automation
    window_title: str = "Comet"
    typing_delay: float = 0.02
    post_focus_delay: float = 0.5
    click_x: int | None = None
    click_y: int | None = None

    model_config = SettingsConfigDict(
        env_prefix="PROMPTCLOCK_",
        env_file=".env",
        extra="ignore",
    )

    @property
    def click_xy(self) -> tuple[int, int] | None:
        if self.click_x is not None and self.click_y is not None:
            return (self.click_x, self.click_y)
        return None


settings = Settings()
