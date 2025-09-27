from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Grocery Store API")

# In-memory database
products = []

# Model
class Product(BaseModel):
    name: str
    price: float
    quantity: int
    in_stock: Optional[bool] = True

@app.get("/")
def home():
    return {"message": "Welcome to Grocery Store API"}

# Create product
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    products.append(product)
    return product

# Read all products
@app.get("/products/", response_model=List[Product])
def list_products():
    return products

# Read single product
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    if product_id < 0 or product_id >= len(products):
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]   # ✅ fix here

# Update product
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    if product_id < 0 or product_id >= len(products):
        raise HTTPException(status_code=404, detail="Product not found")
    products[product_id] = updated_product
    return updated_product

# Delete product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id < 0 or product_id >= len(products):
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = products.pop(product_id)
    return {"message": "Product deleted", "product": deleted}
