
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode , ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode



async def error_log(filename , function_name :str , error_message):
    try:
        from repositories.order_agent_repositories import AgentRepository
        repo = AgentRepository()
        error_id = await repo.create_errorlog(filename , function_name , error_message)
        return error_id
    except CustomAppException:
            raise
    except Exception as e:
            raise CustomAppException(
                message=f"Error in creating error log: {str(e)}",
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
            )


