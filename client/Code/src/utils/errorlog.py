
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode , ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode


def error_log(filename , function_name :str , error_message):
    try:
        from repositories.order_agent_repository import AgentRepository
        repo = AgentRepository()
        error_id = repo.create_errorlog(filename , function_name , error_message)
        return error_id
    
    except Exception as e:
        raise f"Error occured in creating errorlog {str(e)}"
            


