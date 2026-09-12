from fastapi import APIRouter, Query, Body, Depends, Path
from fastapi.responses import JSONResponse 
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from models.api_response_dto import APIResponse
from models.model import UserRequestDTO
from services.order_agent_service import AgentService
from utils.errorlog import error_log
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode , ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode

router = APIRouter(prefix="/training/api", tags=["Cart" , "Product"])



@router.post("/v1/order_agent")
async def agent_route(
    request: UserRequestDTO = Body(...)
):
    try:
        service = AgentService()
        response = await service.agent_service(
            customer_id = request.customer_id ,
            user_query = request.user_query
        )
        result = APIResponse(
                data = str(response),
                code=HttpStatusCode.OK
            )
        return JSONResponse(
            content=jsonable_encoder(result.to_dict()),
            status_code=result.code
        )
    except CustomAppException:
        raise
    except Exception as e:
        
        raise CustomAppException(
            message=f"Router error in processing user query: {str(e)}",
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
            error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
        )