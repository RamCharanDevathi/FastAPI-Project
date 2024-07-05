from fastapi import APIRouter
from fastapi import status, Response, HTTPException
# from Product.routers.login import get_current_user
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from Product import schemas
from Product import models
from Product.database import engine, SessionLocal, get_database



router = APIRouter(
    tags=['Customer'],
    prefix= '/customers'
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def add_customer(request: schemas.CustomerCreate, db: Session = Depends(get_database)):
    try:
        new_customer = models.Customer(**request.dict())
        db.add(new_customer)
        db.commit() 
        db.refresh(new_customer)
        return new_customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/')
def get_all_customer(db: Session = Depends(get_database)):
    customers = db.query(models.Customer).all()
    return customers

@router.get("/single-customer/{customer_id}")
def get_customer(customer_id, db: Session = Depends(get_database)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_database)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_customer.update(customer.dict())
    # db_customer.update(customer.dict())
    
    db.commit()
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_database)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}



@router.get('/{customer_id}', response_model = schemas.Customer)
def get_customers_with_orders(customer_id, db: Session = Depends(get_database)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found")
    return db_customer