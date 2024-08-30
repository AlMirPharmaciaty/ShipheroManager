from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.user_models.user import User
from src.schemas.custom_response import CustomResponse
from src.controllers.user_controllers.auth import Authorize
from src.controllers.shiphero.inventory_snapshot import InventorySnapshotController

inventory_snapshot = APIRouter()


@inventory_snapshot.post("/generate", response_model=CustomResponse)
def generate_inventory_snapshot(db: Session = Depends(get_db),
                                user: User = Depends(Authorize("inventory_snapshot_generate"))):
    """API to generate an inventory snapshot"""
    try:
        controller = InventorySnapshotController(db=db, user=user)
        data = controller.create({'warehouse_id': '1'})
        return CustomResponse(message="Inventory snapshot generated",
                              success=True,
                              data=jsonable_encoder(data))

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to generate snapshot - {str(e)}') from e


@inventory_snapshot.get("/get-status/{snapshot_id}",
                            response_model=CustomResponse)
def get_status(snapshot_id: str,
               db: Session = Depends(get_db),
               _: User = Depends(Authorize("inventory_snapshot_get_status"))):
    """API to get snapshot status"""
    try:
        pass

        return CustomResponse(message="Failed to get status",
                              success=True,
                              data=None)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to mutate - {str(e)}') from e
