from typing import Optional

import pydantic
from pydantic import AnyUrl


class CreateQuestionSchema(pydantic.BaseModel):
    text: str
    answer: str
    url: Optional[AnyUrl]
    forward: Optional[int]
    back: Optional[int]
