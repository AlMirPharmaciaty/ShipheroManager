from sqlalchemy.orm import Session
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from src.config.settings import Settings
from src.utils.id_generator import generate_id
from src.utils.datetime_parser import from_iso
from src.models.user_models.user import User
from src.models.inventory_snapshot import InventorySnapshot
from src.schemas.shiphero_schema import shiphero_schema


settings = Settings()
SHIPHERO_URL = settings.SHIPHERO_URL
SHIPHERO_TOKEN = settings.SHIPHERO_TOKEN


class InventorySnapshotController:
    """Shiphero Orders Controller"""

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user
        self.graphql = HTTPEndpoint(
            SHIPHERO_URL,
            base_headers={'Authorization': f'Bearer {SHIPHERO_TOKEN}'})

    def generate(self, params: dict):
        """Generate an inventory snapshot"""
        op = Operation(shiphero_schema.Mutation)
        mutation = op.inventory_generate_snapshot(data=params)
        mutation.complexity()
        mutation.request_id()
        snapshot = mutation.snapshot()
        snapshot.snapshot_id()
        snapshot.status()
        snapshot.created_at()
        snapshot.updated_at()
        return self.graphql(op)

    def create(self, params: dict):
        """Request a new inventory snapshot"""
        try:
            data = self.generate(params)
            snapshot = data['data']['inventory_generate_snapshot']['snapshot']
            new_snapshot = InventorySnapshot(**snapshot)
            new_snapshot.id = generate_id(self.db, 'is', InventorySnapshot)
            new_snapshot.created_at = from_iso(new_snapshot.created_at)
            new_snapshot.updated_at = from_iso(new_snapshot.updated_at)
            self.db.add(new_snapshot)
            self.db.commit()
            self.db.refresh(new_snapshot)
            return new_snapshot
        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e
