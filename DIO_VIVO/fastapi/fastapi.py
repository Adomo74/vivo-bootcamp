from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB Configuration
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.product_db
product_collection = database.get_collection("products")


# Pydantic Models
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Product(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]


# CRUD Operations
async def add_product(product_data: dict) -> Product:
    try:
        product = await product_collection.insert_one(product_data)
        new_product = await product_collection.find_one({"_id": product.inserted_id})
        return new_product
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erro ao inserir o produto") from e


async def update_product(id: str, product_data: dict) -> Product:
    product_data["updated_at"] = datetime.utcnow().isoformat()
    if len(product_data) >= 1:
        update_result = await product_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": product_data}
        )
        if update_result.modified_count == 1:
            updated_product = await product_collection.find_one({"_id": ObjectId(id)})
            if updated_product is not None:
                return updated_product
    existing_product = await product_collection.find_one({"_id": ObjectId(id)})
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return existing_product


async def filter_products(min_price: float, max_price: float):
    products = await product_collection.find({
        "price": {"$gt": min_price, "$lt": max_price}
    }).to_list(1000)
    return products


# FastAPI Instance
app = FastAPI()


@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate):
    product_data = product.dict()
    product_data["created_at"] = datetime.utcnow().isoformat()
    new_product = await add_product(product_data)
    return new_product


@app.patch("/products/{id}", response_model=Product)
async def update_product_endpoint(id: str, product: ProductUpdate):
    updated_product = await update_product(id, product.dict(exclude_unset=True))
    return updated_product


@app.get("/products/", response_model=List[Product])
async def get_products(min_price: float, max_price: float):
    products = await filter_products(min_price, max_price)
    return products


# Test with Pytest
def test_create_product():
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.post("/products/", json={
        "name": "Product 1",
        "description": "Description 1",
        "price": 100.0
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Product 1"


def test_update_product_not_found():

