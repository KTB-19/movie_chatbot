from typing import Optional

from pydantic import BaseModel

class Recommend(BaseModel):
    message : str