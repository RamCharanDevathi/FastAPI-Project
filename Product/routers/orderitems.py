from fastapi import APIRouter
from fastapi import status, Response, HTTPException
# from Product.routers.login import get_current_user
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from Product import schemas
from Product import models
from datetime import datetime
from Product.database import engine, SessionLocal, get_database


router = APIRouter(
    tags=['OrderItems'],
    prefix='/orderitem'
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def add_orderitem(request: schemas.OrderItemCreate, db: Session = Depends(get_database)):
    try:
        if request.order_id:
            db_order = db.query(models.Orders).filter(models.Orders.id == request.order_id).first()
            if not db_order:
                raise ValueError("Order ID Doesnt Exist")
        if request.product_id:
            db_product = db.query(models.Product).filter(models.Product.id == request.product_id).first()
            if not db_product:
                raise ValueError("Product ID Doesnt Exist")
        new_orderitem = models.OrderItem(**request.dict())
        db.add(new_orderitem)
        db.commit() 
        db.refresh(new_orderitem)
        return new_orderitem
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/')
def get_all_orderitems(db: Session = Depends(get_database)):
    orderitem = db.query(models.OrderItem).all()
    return orderitem

@router.get("/single-orderitem/{orderitem_id}")
def get_orderitem(orderitem_id, db: Session = Depends(get_database)):
    db_orderitem = db.query(models.OrderItem).filter(models.OrderItem.id == orderitem_id).first()
    if db_orderitem is None:
        raise HTTPException(status_code=404, detail="Orderitem not found")
    return db_orderitem

@router.put("/{orderitem_id}")
def update_orderitem(orderitem_id: int, orderitem: schemas.OrderItem, db: Session = Depends(get_database)):
    try:
        db_orderitem = db.query(models.OrderItem).filter(models.OrderItem.id == orderitem_id)

        if not db_orderitem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orderitem not found")
        
        if orderitem.order_id:
            db_order = db.query(models.Orders).filter(models.Orders.id == orderitem.order_id).first()
            if not db_order:
                raise ValueError("Order ID Doesnt Exist")
            
        if orderitem.product_id:
            db_product = db.query(models.Product).filter(models.Product.id == orderitem.product_id).first()
            if not db_product:
                raise ValueError("Product ID Doesnt Exist")
            
        for key, value in orderitem.dict(exclude_unset=True).items():
            setattr(db_orderitem, key, value)

        db.commit()
        return db_orderitem
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{orderitem_id}")
def delete_orderitem(orderitem_id: int, db: Session = Depends(get_database)):
    orderitem = db.query(models.OrderItem).filter(models.OrderItem.id == orderitem_id).first()
    if orderitem is None:
        raise HTTPException(status_code=404, detail="Orderitem not found")
    
    db.delete(orderitem)
    db.commit()
    return {"message": "Orderitem deleted successfully"}