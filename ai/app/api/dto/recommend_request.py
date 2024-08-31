from typing import Optional, List, Dict

from pydantic import BaseModel
from datetime import date, time


class RecommendRequest(BaseModel):
    movieName: str
    date: str
    timesPerTheaterNameMap: Dict[str, List[str]]
