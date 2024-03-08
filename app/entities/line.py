from pydantic import BaseModel
from typing import List, Optional

class LineReply(BaseModel):
    role: str
    content: str