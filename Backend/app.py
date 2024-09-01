from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
    HTTPException,
)

from src import my_app

app = my_app()


@app.exception_handler(RequestValidationError)
async def req_validation_exception_handler(_, e: RequestValidationError):
    """Handling request data validation errors"""
    try:
        if len(e.errors()[0]["loc"]) > 1:
            e = f'{e.errors()[0]["loc"][1]} - {e.errors()[0]["msg"]}'
        e = e.errors()[0]["msg"]
    finally:
        raise HTTPException(status_code=400,
                            detail=f"Validation error - {str(e)}")


@app.exception_handler(ResponseValidationError)
async def res_validation_exception_handler(_, e: ResponseValidationError):
    """Handling response data validation errors"""
    print(e)
    raise HTTPException(status_code=500,
                        detail="Failed to send a valid response")
