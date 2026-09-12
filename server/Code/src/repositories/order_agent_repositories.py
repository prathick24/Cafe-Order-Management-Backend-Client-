from sqlalchemy.orm import  joinedload 
from sqlalchemy import desc, asc , or_
from decimal import Decimal
from typing import List, Optional, Tuple ,Any , Dict
from uuid import UUID
from datetime import datetime , date
from repositories.schemas.schema import Order , Order_item , Item , Errorlog
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode
from repositories.database import Database 
from utils.errorlog import error_log


class AgentRepository:
    def __init__(self):
        self.db_instance = Database()

    def list_menu(self):
        db_session = self.db_instance.SessionLocal()
        try:
            items = db_session.query(Item.item_name , Item.item_price).all()
            return [{"name":i.item_name , "price" :float(i.item_price)} for i in items]
        except CustomAppException:
            raise
        except Exception as e:
            error_log("repository.py" , "list_menu" , e)
            raise CustomAppException(
                message=f"Database error getting menu items: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
            )
        finally:
            db_session.close()
    
        

    def create_order(self ,user_id , items):
        try:
            db_session = self.db_instance.SessionLocal()
            price = 0
            product_ids =[]
            items_quantity =[]
            for item in items:
                id = db_session.query(Item.item_id).filter(Item.item_name.ilike(f"%{item.item_name}%")).first()
                product_ids.append(id[0])

                if not id :
                    raise CustomAppException(
                        message=f"Sorry for the inconvience , The item that you have ordered is not available in our restaurent",
                        code=ErrorCode.PRODUCT_NOT_FOUND,
                        status_code=HttpStatusCode.NOT_FOUND,
                        error_code_id=ErrorCodeStatus[ErrorCode.PRODUCT_NOT_FOUND]
                    )
                item_price = db_session.query(Item.item_price).filter(Item.item_name == item.item_name).scalar()
                price += item_price or Decimal('0')

                items_quantity.append(item.quantity)
            
            new_order = Order(
                customer_id = user_id ,
                total_price = price
            )
            db_session.add(new_order)
            db_session.flush()

            for i in range(len(product_ids)):
                
                new_order_items = Order_item(
                    order_id = new_order.order_id,
                    item_id = product_ids[i],
                    quantity = items_quantity[i]
                )
            db_session.add(new_order_items)
            db_session.flush()
            db_session.commit()
            return {
                "order_id":new_order.order_id,
                "total_price":price
            }
        except CustomAppException:
            raise
        except Exception as e:
            error_log("repository.py" , "create_order" , e)
            raise CustomAppException(
                    message=f"Database error placing order: {str(e)}",
                    code=ErrorCode.DATABASE_ERROR,
                    status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                    error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
            )
        finally:
            db_session.close()

    def get_status(self , order_id : int):
        try:
            db_session = self.db_instance.SessionLocal()

            status = db_session.query(Order.order_status).filter(Order.order_id == order_id).first()
            if not status:
                 return f"Order Id not present"
            else:
                  return status[0]
  
        except CustomAppException:
                raise
        except Exception as e:
                error_log("repository.py" , "get_status" , e)
                raise CustomAppException(
                        message=f"Database error getting order status: {str(e)}",
                        code=ErrorCode.DATABASE_ERROR,
                        status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                        error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
                )
        finally:
            db_session.close()

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
                error_log("repository.py" , "create_errorlog" , e)
                raise CustomAppException(
                        message=f"Database error creating errorlog: {str(e)}",
                        code=ErrorCode.DATABASE_ERROR,
                        status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                        error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
                )
        finally:
            db_session.close()




    
        

    