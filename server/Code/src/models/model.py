from pydantic import BaseModel , Field 
from typing import Optional , List

class UserRequestDTO(BaseModel):
    user_query : str = Field(description= "query asked by the user")

class OrderItem(BaseModel):
    item_name : str
    quantity : int

class Order(BaseModel):
    items : List[OrderItem]

