from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str
    short_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def short_url(self) -> str:
        # Пока используем заглушку localhost:8080. На Render заменим через ENV переменную
        return f"http://localhost:8080/r/{self.short_name}"

class LinkCreate(SQLModel):
    original_url: str
    short_name: str

class LinkUpdate(SQLModel, validate_on_call=True):
    original_url: Optional[str] = None
    short_name: Optional[str] = None




