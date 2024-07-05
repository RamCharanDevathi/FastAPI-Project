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
    tags=['Supplier'],
    prefix='/suppliers'
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def add_supplier(request: schemas.SupplierCreate, db: Session = Depends(get_database)):
    new_supplier = models.Supplier(**request.dict())
    db.add(new_supplier)
    db.commit() 
    db.refresh(new_supplier)
    return new_supplier


@router.get('/')
def get_all_suppliers(db: Session = Depends(get_database)):
    supplier = db.query(models.Supplier).all()
    return supplier

@router.get("/single-supplier/{supplier_id}")
def get_supplier(supplier_id, db: Session = Depends(get_database)):
    db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="supplier not found")
    return db_supplier

@router.put("/{supplier_id}")
def update_supplier(supplier_id: int, supplier: schemas.SupplierBase, db: Session = Depends(get_database)):
    db_supplier= db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="supplier not found")
    
    db_supplier.update(supplier.dict())
    
    db.commit()
    return {'supplier updated successfully'}

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_database)):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not supplier :
        raise HTTPException(status_code=404, detail="supplier not found")
    
    db.delete(supplier)
    db.commit()
    return {"message": "supplier deleted successfully"}

@router.get('/{supplier_id}', response_model = schemas.Supplier)
def get_supplier_with_products(supplier_id, db: Session = Depends(get_database)):
    db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not db_supplier :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="supplier not found")
    return db_supplier