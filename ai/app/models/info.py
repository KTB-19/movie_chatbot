from typing import Optional, List

from pydantic import BaseModel

class Info(BaseModel):
    movieName : Optional[str]
    region : Optional[List[str]]
    date : Optional[str]
    time : Optional[str]
    response : Optional[str]