from fastapi.exceptions import RequestValidationError, HTTPException

from src import my_app

app = my_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, e: RequestValidationError):
    """Handling data validation errors"""
    try:
        if len(e.errors()[0]["loc"]) > 1:
            e = f'{e.errors()[0]["loc"][1]} - {e.errors()[0]["msg"]}'
        e = e.errors()[0]["msg"]
    finally:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error - {str(e)}")
