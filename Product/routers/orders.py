from fastapi import APIRouter
from fastapi import status, Response, HTTPException
# from Product.routers.login import get_current_user
from fastapi.params import Depends
from sqlalchemy.orm import Session
from Product.routers.login import get_current_user
from typing import List
from Product import schemas
from Product import models
from datetime import datetime
from Product.database import engine, SessionLocal, get_database


router = APIRouter(
    tags=['Orders'],
    prefix='/orders'
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def add_order(request: schemas.OrderCreate, db: Session = Depends(get_database)):
    try:
        if request.customer_id:
            db_customer = db.query(models.Customer).filter(models.Customer.id == request.customer_id).first()
            if not db_customer:
                raise ValueError("Customer ID Doesnt Exist")
        new_order = models.Orders(**request.dict())
        db.add(new_order)
        db.commit() 
        db.refresh(new_order)
        return new_order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/')
def get_all_orders(db: Session = Depends(get_database)):
    orders = db.query(models.Orders).all()
    return orders

@router.get("/single-order/{order_id}")
def get_order(order_id, db: Session = Depends(get_database)):
    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}")
def update_order(order_id: int, order: schemas.Order, db: Session = Depends(get_database)):
    try:
        db_order = db.query(models.Orders).filter(models.Orders.id == order_id)

        if not db_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        if order.customer_id:
            db_customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
            if not db_customer:
                raise ValueError("Customer ID does not exist")
            
        for key, value in order.dict(exclude_unset=True).items():
            setattr(db_order, key, value)

        db.commit()
        return db_order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{order_id}/status")
def update_order_status(order_id: int, status: schemas.OrderUpdateStatus, db: Session = Depends(get_database)):
    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Order not found")
    db_order.status = status.status
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}/items", response_model=List[schemas.OrderItem])
def list_order_items(order_id: int, db: Session = Depends(get_database)):
    order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order.orderitem


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_database)):
    order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

@router.get('/{order_id}', response_model = schemas.Order)
def get_orders_with_customers(order_id, db: Session = Depends(get_database)):
    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if not db_order :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return db_order