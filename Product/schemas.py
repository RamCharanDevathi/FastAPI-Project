from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import List, Optional


class statusEnum(str, Enum):
    pending = 'Pending'
    fulfilled = 'Fulfilled'
    cancelled = 'Cancelled'

'''
class Product(BaseModel):
    prod_name: str
    description: str
    price: int
    stock: int

class DisplaySupplier(BaseModel):
    id:int
    supl_name: str

    class Config:
        orm_mode = True
    
class DisplayProduct(BaseModel):
    id: int
    prod_name: str

    class Config:
        orm_mode = True

class Supplier(BaseModel):
    id: int
    supl_name: str
    contact_info: str
    password: str


class Customer(BaseModel):
    cust_name: str
    contact_info : str

class CustomerUpdate(Customer):
    pass

class DisplayCustomer(BaseModel):
    name: str
    contact_info :str

    class Config:
        orm_mode = True


class Orders(BaseModel):
    customer_id : int
    order_date : date
    status:  statusEnum

'''



class LoginBase(BaseModel):
    username: str


class LoginCreate(LoginBase):
    password: str

class Login(LoginBase):
    id: int
    username: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : Optional[str] = None

    
# Product schemas
class ProductBase(BaseModel):
    prod_name: str
    description: Optional[str] = None
    price: int
    supplier_id: int
    stock: Optional[int] = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    supplier_id: Optional[int] = None
    stock: Optional[int] = None

    class Config:
        orm_mode = True

class Product(ProductBase):
    id: int
    supplier_id: int

    class Config:
        orm_mode = True

# Supplier schemas
class SupplierBase(BaseModel):
    supl_name: str
    contact_info: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int
    products: List[Product] = []

    class Config:
        orm_mode = True

# Customer schemas
class CustomerBase(BaseModel):
    cust_name: str
    contact_info: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

# Order schemas
class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True

# order schemas
class OrderBase(BaseModel):
    customer_id: int
    order_date: date
    status: statusEnum

class OrderCreate(OrderBase):
    pass
    # order_items: List[OrderItemCreate]

class OrderUpdateStatus(BaseModel):
    status: statusEnum

class Order(OrderBase):
    id: int
    order_items: List[OrderItem] = []
    shipment: Optional['Shipment']

    class Config:
        orm_mode = True

class Customer(CustomerBase):
    id: int
    name: str
    contact_info: str
    orders: List[Order] = []

    class Config:
        orm_mode = True

# Shipment schemas
class ShipmentBase(BaseModel):
    order_id: int
    shipment_date: Optional[date] = None
    delivery_date: Optional[date] = None
    status: Optional[str] = None

class ShipmentCreate(ShipmentBase):
    pass

class Shipment(ShipmentBase):
    id: int

    class Config:
        orm_mode = True