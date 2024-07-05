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
    tags=['shipment'],
    prefix='/shipment'
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def add_shipment(request: schemas.ShipmentCreate, db: Session = Depends(get_database)):
    try:
        if request.order_id:
            db_order = db.query(models.Orders).filter(models.Orders.id == request.order_id).first()
            if not db_order:
                raise ValueError("Order ID Doesnt Exist")

        new_shipment = models.OrderItem(**request.dict())
        db.add(new_shipment)
        db.commit() 
        db.refresh(new_shipment)
        return new_shipment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/')
def get_all_shipments(db: Session = Depends(get_database)):
    shipments = db.query(models.Shipment).all()
    return shipments

@router.get("/single-orderitem/{shipment_id}")
def get_shipment(shipment_id, db: Session = Depends(get_database)):
    db_shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment

@router.put("/{shipment_id}")
def update_shipment(shipment_id: int, shipment: schemas.Shipment, db: Session = Depends(get_database)):
    try:
        db_shipments = db.query(models.Shipment).filter(models.Shipment.id == shipment_id)

        if not db_shipments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="shipment not found")
        
        if shipment.order_id:
            db_order = db.query(models.Orders).filter(models.Orders.id == shipment.order_id).first()
            if not db_order:
                raise ValueError("Order ID Doesnt Exist")

            
        for key, value in shipment.dict(exclude_unset=True).items():
            setattr(db_shipments, key, value)

        db.commit()
        return db_shipments
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(get_database)):
    shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    db.delete(shipment)
    db.commit()
    return {"message": "Shipment deleted successfully"}