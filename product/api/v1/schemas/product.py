from pydantic import BaseModel, Field


class PlaceOrderRequestSchema(BaseModel):
    product_id: int = Field(..., description="product_id")
    quantity: int = Field(..., description="quantity")


class PlaceOrderResponseSchema(BaseModel):
    order_id: str
    message: str


class UpdateOrderRequestSchema(BaseModel):
    quantity: int = Field(..., description="quantity")


class UpdateOrderResponseSchema(BaseModel):
    order_id: str
    message: str
