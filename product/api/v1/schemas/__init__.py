from .product import *


class ExceptionResponseSchema(BaseModel):
    # error: str
    __root__: dict


class SuccessfulResponseSchema(BaseModel):
    __root__: dict
