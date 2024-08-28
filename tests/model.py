from pydantic import BaseModel, Field
from typing import Optional, List


class RequestStructure(BaseModel):
    id_: int = Field(alias='id')
    project_tasks_resource_id: int
    volume: float
    cost: float
    batch_number: Optional[int] = None
    batch_parent_request_id: Optional[int] = None
    is_over_budget: bool
    created_at: int
    updated_at: int
    user_id: int
    needed_at: int
    created_by: int


class ListRequestStructure(BaseModel):
    full_list: List[RequestStructure]

