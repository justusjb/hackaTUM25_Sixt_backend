from pydantic import BaseModel
from typing import Dict, List, Optional


class CustomerData(BaseModel):
    name: str
    destination: str
    party_size: int
    previous_rentals: List[str]
    booking_date: str


class QuestionNode(BaseModel):
    id: int
    key: str
    question: str
    image: str
    yes: Optional[str] = None
    no: Optional[str] = None


class TreeResponse(BaseModel):
    tree: Dict[str, QuestionNode]
