from repositories.order_agent_repositories import AgentRepository
from routes.order_agent_route import router
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode , ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode
from utils.errorlog import error_log
import json


repo = AgentRepository()
    
@router.resource("menu://all",description= "Return all the items in menu")    
def get_menu():
        """This resource helps in getting the menu for user reference"""
        try:
            menu = repo.list_menu()
            return json.dumps(menu , indent = 2)
        except CustomAppException:
            raise
        except Exception as e:
            
            raise CustomAppException(
                message=f"Tool Error in getting menu: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
            )
@router.resource("policy://shop")
def company_policy():
    """This resouces helps in getting the company policy"""
    return"""
   Operating Hours:
    this cafe will be from 8 AM to 10 PM in weekdays
    In weekends , cafe will be from 10 AM to 9PM

    Offers:
    Customer who visits on their Birthday will get a free cake
    On every summer , the Cold juices will be served as buy 1 get 1

    cafe Address:
    123 , Wall of jessie
    Albequerque , Mexico
    """

