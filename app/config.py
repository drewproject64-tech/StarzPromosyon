from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_id: int | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise RuntimeError("BOT_TOKEN environment variable is required")

        raw_admin = os.getenv("ADMIN_ID", "").strip()
        admin_id = int(raw_admin) if raw_admin else None
        return cls(bot_token=token, admin_id=admin_id)
