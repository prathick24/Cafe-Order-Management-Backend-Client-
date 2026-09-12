from repositories.database import Database 
from utils.errorlog import error_log
from repositories.schemas.schema import Errorlog
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode , ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode

class AgentRepository:
    def __init__(self):
        self.db_instance = Database()
    
    def create_errorlog(self ,filename :str , function_name :str , error_message :str):
        db_session = self.db_instance.SessionLocal()
        try:
            new_error = Errorlog(
                filename = filename ,
                function_name = function_name ,
                error_message = error_message
            )
            db_session.add(new_error)
            db_session.flush()
            db_session.commit()
            return new_error.error_log_id
        except CustomAppException:
                raise
        except Exception as e:
                raise CustomAppException(
                        message=f"Database error creating errorlog: {str(e)}",
                        code=ErrorCode.DATABASE_ERROR,
                        status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                        error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
                )
        
        finally:
            db_session.close()