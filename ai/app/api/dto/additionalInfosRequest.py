from typing import Optional

from pydantic import BaseModel


class QueryDto(BaseModel):
    movieName: Optional[str]
    region: Optional[str]
    date: Optional[str]


class QueriesDto(BaseModel):
    movieNameQuery: Optional[str]
    regionQuery: Optional[str]
    dateQuery: Optional[str]


class AdditionalInfosRequest(BaseModel):
    parsedQuery: QueryDto
    additionQueries: QueriesDto
