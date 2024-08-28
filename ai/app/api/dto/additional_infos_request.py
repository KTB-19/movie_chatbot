from typing import Optional

from pydantic import BaseModel


class QueryDto(BaseModel):
    movieName: Optional[str]
    region: Optional[str]
    date: Optional[str]
    time: Optional[str]


class AdditionalInfosRequest(BaseModel):
    parsedQuery: QueryDto
    message: str
