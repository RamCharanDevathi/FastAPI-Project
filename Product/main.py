from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import get_database, engine
from .models import Base, Product
from Product.routers import customers, orders, products, suppliers, orderitems, shipment, login
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Supply Chain API",
    description="API's to perfrom the supply chain operations"
)

app.include_router(login.router)
app.include_router(suppliers.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(orderitems.router)
app.include_router(shipment.router)
# app.include_router(login.router)

'''
# models defined are converted into tables in the database
models.Base.metadata.create_all(engine)
@app.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_database)):
    db_product = Product(**product.dict())
    return crud.create_product(db=db, product=db_product)

@app.get("/products/", response_model=List[ProductSchema])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_database)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_database)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_database)):
    crud.update_product(db, product_id=product_id, product_data=product.dict())
    return crud.get_product(db, product_id=product_id)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_database)):
    crud.delete_product(db, product_id=product_id)
    return {"detail": "Product deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

'''
