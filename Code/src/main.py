import uvicorn
# ==================== FASTAPI IMPORTS ====================
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.order_agent_route import router
from models.api_response_dto import APIResponse, Error
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode
 


# ==================== FASTAPI mainLICATION INITIALIZATION ====================
main = FastAPI(
    title="Order Agent API",
    description="REST API for Order Agent",
    version="1.0.0",
)

# SQ_1.18 to 1.19 fetch_groups
# ==================== MIDDLEWARE CONFIGURATION ====================
main.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

main.include_router(router)


# ==================== EXCEPTION HANDLERS ====================
@main.exception_handler(CustomAppException)
async def custom_exception_handler(request: Request, exc: CustomAppException):
    api_response = exc.to_api_response()
    return JSONResponse(
        status_code=exc.status_code,
        content=api_response.to_dict()
    )

@main.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append(Error(
            code=ErrorCode.VALIDATION_ERROR,
            message=f"{error['loc'][-1]}: {error['msg']}",
            error_code_id=ErrorCodeStatus[ErrorCode.VALIDATION_ERROR]
        ))
    
    api_response = APIResponse(
        data=None,
        errors=errors,
        code=HttpStatusCode.UNPROCESSABLE_ENTITY
    )
    
    return JSONResponse(
        status_code=HttpStatusCode.UNPROCESSABLE_ENTITY,
        content=api_response.to_dict()
    )

# ==================== APPLICATION ENTRY POINT ====================
if __name__ == "__main__":
    """
    Main entry point for running the FastAPI application locally.
    """
    uvicorn.run(
        "main:main",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )