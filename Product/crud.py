from sqlalchemy.orm import Session
from .models import Product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product_id: int, product_data: dict):
    db.query(Product).filter(Product.id == product_id).update(product_data)
    db.commit()

def delete_product(db: Session, product_id: int):
    db.query(Product).filter(Product.id == product_id).delete()
    db.commit()
