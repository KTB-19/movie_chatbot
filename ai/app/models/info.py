from typing import Optional

from pydantic import BaseModel

class Info(BaseModel):
    movieName : Optional[str]
    region : Optional[str]
    date : Optional[str]
    time : Optional[str]
    response : Optional[str]