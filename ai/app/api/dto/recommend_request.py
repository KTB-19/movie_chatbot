from typing import Optional, List, Dict

from pydantic import BaseModel
from datetime import date, time


class RecommendRequest(BaseModel):
    movieName: str
    region: str
    date: str
    time: Optional[str]
    timesPerTheaterNameMap: Dict[str, List[str]]
