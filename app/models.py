from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Link(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    short_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def short_url(self) -> str:
        
        return f"http://localhost:8080/r/{self.short_name}"

class LinkCreate(SQLModel):
    original_url: str
    short_name: str

class LinkUpdate(SQLModel, validate_on_call=True):
    original_url: str | None = None
    short_name: str | None = None




