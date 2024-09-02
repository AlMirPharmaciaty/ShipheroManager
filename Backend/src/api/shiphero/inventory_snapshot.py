import threading
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.user_models.user import User
from src.models.shiphero.inventory_snapshot import InventorySnapshot
from src.schemas.custom_response import CustomResponse
from src.schemas.shiphero.inventory_snapshot import (
    InventorySnapshotCreate,
    InventorySnapshotResponseModel)
from src.controllers.user_controllers.auth import Authorize
from src.controllers.shiphero.inventory_snapshot import (
    InventorySnapshotController)

inventory_snapshot = APIRouter()


@inventory_snapshot.post("/", response_model=InventorySnapshotResponseModel)
def generate_inventory_snapshot(
        params: InventorySnapshotCreate,
        db: Session = Depends(get_db),
        user: User = Depends(Authorize("inventory_snapshot_create"))):
    """API to generate an inventory snapshot"""
    try:
        controller = InventorySnapshotController(db=db, user=user)
        data = controller.create(params)
        return CustomResponse(message="Inventory snapshot generated",
                              success=True,
                              data=data)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to generate inventory snapshot - {str(e)}') from e


@inventory_snapshot.get('/', response_model=InventorySnapshotResponseModel)
def get_all_snapshots(query: str = None,
                      db_id: int = None,
                      status: str = None,
                      sort_by: str = "created_at",
                      sort_order: str = "desc",
                      page: int = 1,
                      limit: int = 10,
                      db: Session = Depends(get_db),
                      _: User = Depends(Authorize("inventory_snapshot_read"))):
    """API to retrieve all inventory snapshots from database"""
    try:
        controller = InventorySnapshotController(db=db)
        snapshots, pagination = controller.read_many(query=query,
                                                     db_id=db_id,
                                                     status=status,
                                                     sort_by=sort_by,
                                                     sort_order=sort_order,
                                                     page=page,
                                                     limit=limit)
        return CustomResponse(success=True,
                              data=snapshots,
                              pagination=pagination)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to retrieve inventory snapshots - {str(e)}') from e


@inventory_snapshot.patch("/", response_model=InventorySnapshotResponseModel)
def update_snapshot(snapshot_db_id: int | None = None,
                    db: Session = Depends(get_db),
                    user: User = Depends(Authorize("inventory_snapshot_update"))):
    """
    API to update snapshot status
    -   snapshot_db_id = database id, not shiphero id
    -   If snapshot id given,
        read and update if the snapshot status is not "success"
    -   if snapshot id not given,
        get and update all snapshots from database
        where status is either "pending", "enqueued", or "processing"
    """
    try:
        controller = InventorySnapshotController(db=db, user=user)
        response = CustomResponse(success=True)
        if snapshot_db_id:
            snapshot: InventorySnapshot = controller.read(snapshot_db_id)
            if snapshot.status in ["success", "error", "abort"]:
                response.data = snapshot
                response.message = "Inventory snapshot is up to date"
            else:
                response.data = controller.update(snapshot_db_id)
                response.message = "Successfully updated snapshot"

        else:
            limit = 100
            page = 1
            status = "enqueued,pending,processing"
            s, p = controller.read_many(status=status, limit=limit)
            if p.filtered == 0:  # If no snapshot with given status
                response.message = "All snapshots are up to date"
            else:
                snapshot_ids = [snapshot.id for snapshot in s]
                next_page = p.filtered > len(s)  # check for more snapshots
                while next_page:
                    page += 1
                    s, p = controller.read_many(status=status,
                                                limit=limit, page=page)
                    for snapshot in s:
                        snapshot_ids.append(snapshot.id)
                    next_page = p.filtered > len(snapshot_ids)
                threading.Thread(target=controller.update_many,
                                 args=(snapshot_ids,)).start()
                response.message = f"Updating {p.filtered} snapshots"
        return response

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to update inventory snapshot - {str(e)}') from e
