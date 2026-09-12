from typing import Dict
from agents.agent import OrderAgent
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode , ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode


import os

class AgentService:
    def __init__(self):
        self.agent = OrderAgent()
    async def agent_service(
            self,
            customer_id : int,
            user_query : str
    ):
        try:
            result = await self.agent.create_mcp_agent(customer_id , user_query)  
            return result
        except CustomAppException:
                raise
        except Exception as e:
                
                raise CustomAppException(
                        message=f"Database error creating errorlog: {str(e)}",
                        code=ErrorCode.DATABASE_ERROR,
                        status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                        error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
                )