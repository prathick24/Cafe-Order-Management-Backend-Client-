from langchain_core.tools import tool
from repositories.order_agent_repositories import AgentRepository
from models.model import Order , OrderItem
from typing import List
from routes.order_agent_route import router
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode , ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode
from utils.errorlog import error_log
import json

repo = AgentRepository()
    
@router.tool()
def place_order( customer_id , items: List[OrderItem])-> str:
    """
    Place an order for one or multiple items for the customer.
    Args:
        customer_id : ID of the customer who placed the order - strictly use ID for ordering not the name
        items (List[OrderItem]): List of items where each item has:
            - item_name (str): Exact name of the item as shown in the menu
            - quantity (int): Number of units to order (must be greater than 0)
    Use this tool when:
    - User wants to place an order
    - User says 'I want to order...'
    - User orders multiple items at once
    Rules:
    - Always call list_menu first to verify item exists before placing order
    - If the user ordered item is not in the menu , suggest another item that is present in the menu
    - Do not hallucinate and suggest an item
    - Never place an order for items not in the menu
    - If item name is unclear, ask the customer to clarify
    """
    try:
       order = repo.create_order(customer_id ,items)
       return f"Your order has been placed with the order_id '{order["order_id"]} and the total price is {order["total_price"]}'.Thanks for coming" 
    except CustomAppException:
       raise
    except Exception as e:
        error_log("tool.py" , "place_order" , e)
        raise CustomAppException(
                message=f"Tool Error in placing order: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
            )
@router.tool()
def order_status(order_id : int):
    """Retrive and display the status of the order for the provided order_id
    Use tool when:
    -user asks can I know the status of my order id 2
    -User needs to know the status of their order
    -Do not hallucinate and provide false information
    -Reply kindly to the User
    Args:
        order_id : int Order id provided by the user


    Rules:
    - If the returned status or order_id is none just reply politely
    """
    try:
        
        status = repo.get_status(order_id)
        return f"The current status of your order is{status}"
    except CustomAppException:
       raise
    except Exception as e:
        
        raise CustomAppException(
                message=f"Tool Error in retriving status: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
            )


    
       
