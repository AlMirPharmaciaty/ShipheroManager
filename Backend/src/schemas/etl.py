from datetime import date
from pydantic import BaseModel, Field


class ExtractFilters(BaseModel):
    from_date: date | None = str(date.today())
    limit_per_request: int | None = Field(default=10, min=1, max=100)
