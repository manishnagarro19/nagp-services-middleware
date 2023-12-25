import logging
from fastapi import APIRouter, HTTPException
from proto.order_pb2 import OrderRequest

from api.v1.order_service_grpc import order_service_stub

from api.v1.schemas import (
    ExceptionResponseSchema,
    PlaceOrderRequestSchema,
    PlaceOrderResponseSchema,
    UpdateOrderRequestSchema,
    UpdateOrderResponseSchema,
)

product_router = APIRouter()

logger = logging.getLogger("product-application")


@product_router.post(
    "/place_order",
    response_model=PlaceOrderResponseSchema,
    responses={
        "400": {"model": ExceptionResponseSchema},
        "200": {"description": "Place order"},
    },
)
async def place_order(product_req: PlaceOrderRequestSchema):
    try:
        # Call gRPC service to place order
        product_id = product_req.product_id
        quantity = product_req.quantity
        request = OrderRequest(product_id=product_id, quantity=quantity)
        response = order_service_stub.PlaceOrder(request)

        return {
            "message": "Your order has been successfully placed.",
            "order_id": response.order_id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error placing order: {str(e)}")


@product_router.put(
    "/update_order/{order_id}",
    response_model=UpdateOrderResponseSchema,
    responses={
        "400": {"model": ExceptionResponseSchema},
        "200": {"description": "Update order"},
    },
)
async def update_order(order_id: str, product_req: UpdateOrderRequestSchema):
    try:
        # Call gRPC service to place order
        quantity = product_req.quantity
        product_id = product_req.product_id
        request = OrderRequest(
            order_id=order_id, product_id=product_id, quantity=quantity
        )
        response = order_service_stub.UpdateOrder(request)

        return {
            "message": "The order has been successfully updated.",
            "order_id": order_id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error placing order: {str(e)}")
