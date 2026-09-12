from sqlalchemy import Column, Integer, text, DateTime, String, ForeignKey, Boolean, Numeric , CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    customer_uuid = Column(String, server_default=text("gen_random_uuid()"), unique=True, index=True)
    customer_name = Column(String , nullable = False)
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String, default="SYSTEM")
    modified_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(String, default="SYSTEM")


class Item(Base):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True, index=True)
    item_uuid = Column(String, server_default=text("gen_random_uuid()"), unique=True, index=True)
    item_name = Column(String , nullable = False)
    item_price = Column(Numeric(7,2) , nullable = False)
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String, default="SYSTEM")
    modified_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(String, default="SYSTEM")

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    order_uuid = Column(String, server_default=text("gen_random_uuid()"), unique=True, index=True)
    customer_id = Column(Integer , ForeignKey("customers.customer_id"))
    total_price = Column(Numeric(7,2) , nullable = False)
    order_status = Column(String, CheckConstraint("order_status IN ('ORDERED' , 'PREPARING' , 'DELIVERED')"),default="ORDERED"  )
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String, default="SYSTEM")
    modified_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(String, default="SYSTEM")

class Order_item(Base):
    __tablename__ = "order_items"
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_item_uuid = Column(String, server_default=text("gen_random_uuid()"), unique=True, index=True)
    order_id = Column(Integer,  ForeignKey("orders.order_id"))
    item_id = Column(Integer,  ForeignKey("items.item_id"))
    quantity = Column(Integer , nullable = False)
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String, default="SYSTEM")
    modified_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(String, default="SYSTEM")

class Errorlog(Base):
    __tablename__ = "errorlogs"
    error_log_id = Column(Integer, primary_key=True, index=True)
    error_log_uuid = Column(String, server_default=text("gen_random_uuid()"), unique=True, index=True)
    filename = Column(String , nullable = False)
    function_name = Column(String , nullable= False)
    error_message = Column(String , nullable=False)
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String, default="SYSTEM")
    

    

     