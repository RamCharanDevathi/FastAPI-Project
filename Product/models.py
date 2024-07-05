from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from Product.database import Base

class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True, index=True)
    supl_name = Column(String(100))
    contact_info = Column(String(30))

    products = relationship("Product", back_populates="supplier")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    prod_name = Column(String(100), index=True)
    description = Column(String(255))
    price = Column(Integer)
    stock = Column(Integer)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))

    supplier = relationship("Supplier", back_populates="products")
    orderitem = relationship("OrderItem", back_populates="products")


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, index=True)
    cust_name = Column(String(200))
    contact_info = Column(String(200))

    orders = relationship("Orders",back_populates="customer")

class Login(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(200))
    password = Column(String(200))


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date)
    status = Column(Enum('Pending','Fulfilled','Cancelled', name='order_status'))
    customer_id = Column(Integer, ForeignKey('customer.id'))

    customer = relationship("Customer", back_populates="orders")
    shipment = relationship("Shipment", back_populates="orders")
    orderitem = relationship("OrderItem", back_populates="orders")


class Shipment(Base):
    __tablename__ = 'shipment'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    shipment_date = Column(Date)
    delivery_date = Column(Date)
    status = Column(Enum('Shipped','In Transit', 'Delivered', 'Returned'))

    orders = relationship("Orders",back_populates="shipment")

class OrderItem(Base):
    __tablename__ = 'orderitem'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Integer)

    orders = relationship("Orders", back_populates="orderitem")
    products = relationship("Product", back_populates="orderitem")