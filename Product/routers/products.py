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
from Product.routers.login import get_current_user


router = APIRouter(
    tags=['Products'],
    prefix='/products'
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def add_product(request: schemas.ProductCreate, db: Session = Depends(get_database)):
    try:
        if request.supplier_id:
            db_supplier = db.query(models.Supplier).filter(models.Supplier.id == request.supplier_id).first()
            if not db_supplier:
                raise ValueError("Supplier ID does not exist")
        new_product = models.Product(**request.dict())
        db.add(new_product)
        db.commit() 
        db.refresh(new_product)
        return new_product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/')
def get_all_products(db: Session = Depends(get_database),current_user:schemas.Login = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products

@router.get("/single-product/{product_id}")
def get_product(product_id, db: Session = Depends(get_database)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return db_product

@router.put("/{product_id}")
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_database),current_user:schemas.Login = Depends(get_current_user)):
    try:
        db_product= db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        if product.supplier_id:
            db_supplier = db.query(models.Supplier).filter(models.Supplier.id == product.supplier_id).first()
            if not db_supplier:
                raise ValueError("Supplier ID does not exist")
            
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)

        db.commit()
        # db.refresh(db_product)
        return db_product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_database),current_user:schemas.Login = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "product deleted successfully"}


@router.get('/{product_id}', response_model = schemas.Product)
def get_products_with_supplier(product_id, db: Session = Depends(get_database)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return db_product
