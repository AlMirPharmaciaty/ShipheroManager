import threading
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controllers.user_controllers.auth import Authorize
from src.controllers.etl.extract import Extractor, ShipheroQueriesEnum
from src.schemas.custom_response import CustomResponse
from src.schemas.etl import ExtractFilters
from src.models.user_models.user import User

etl = APIRouter()


@etl.post("/extract", response_model=CustomResponse)
def extract(query: ShipheroQueriesEnum,
            filters: ExtractFilters | None = ExtractFilters(),
            db: Session = Depends(get_db),
            user: User = Depends(Authorize(permission="etl_extract"))):
    """API to extract date from shiphero"""
    try:
        controller = Extractor(db=db)
        threading.Thread(target=controller.extract,
                         args=(user, query, filters,)).start()
        return CustomResponse(message="Extraction started...", success=True)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to start data extraction - {str(e)}') from e
