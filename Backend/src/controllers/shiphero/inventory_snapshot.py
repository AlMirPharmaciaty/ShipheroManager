from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from src.config.settings import Settings
from src.utils.id_generator import generate_id
from src.utils.datetime_parser import from_iso
from src.models.user_models.user import User
from src.models.shiphero.inventory_snapshot import InventorySnapshot
from src.schemas.custom_response import Pagination
from src.schemas.shiphero_schema import shiphero_schema
from src.schemas.shiphero.inventory_snapshot import InventorySnapshotCreate


settings = Settings()
SHIPHERO_URL = settings.SHIPHERO_URL
SHIPHERO_TOKEN = settings.SHIPHERO_TOKEN


class InventorySnapshotController:
    """Shiphero Inventory Snapshot Controller"""

    def __init__(self, db: Session, user: User | None = None):
        self.db = db
        self.user = user
        self.graphql = HTTPEndpoint(
            SHIPHERO_URL,
            base_headers={'Authorization': f'Bearer {SHIPHERO_TOKEN}'})

    def build_query(self, query):
        """Shiphero graphql query for inventory snapshot"""
        query.complexity()
        query.request_id()
        snapshot = query.snapshot()
        snapshot.snapshot_id()
        snapshot.status()
        snapshot.created_at()
        snapshot.updated_at()
        snapshot.snapshot_url()
        snapshot.snapshot_expiration()
        snapshot.job_user_id()
        snapshot.job_account_id()
        snapshot.warehouse_id()
        snapshot.customer_account_id()
        snapshot.notification_email()
        snapshot.email_error()
        snapshot.post_url()
        snapshot.post_error()
        snapshot.post_url_pre_check()
        snapshot.error()
        snapshot.enqueued_at()

    def generate(self, params: InventorySnapshotCreate):
        """Generate an inventory snapshot"""
        params = params.model_dump()
        params = {key: val for key, val in params.items() if val != None}
        op = Operation(shiphero_schema.Mutation)
        self.build_query(op.inventory_generate_snapshot(data=params))
        data = self.graphql(op)
        if "errors" in data:
            raise Exception(str(data['errors'][0]['message']))
        return data['data']['inventory_generate_snapshot']['snapshot']

    def extract(self, snapshot_id: str):
        """Extract a snapshot by id"""
        op = Operation(shiphero_schema.Query)
        self.build_query(op.inventory_snapshot(snapshot_id=snapshot_id))
        data = self.graphql(op)
        if "errors" in data:
            raise Exception(str(data['errors'][0]['message']))
        return data['data']['inventory_snapshot']['snapshot']

    def extract_many(self, params: dict):
        """Extract multiple snapshots"""
        pass

    def transform(self, snapshot: dict):
        """Transform the raw inventory snapshot extracted from shiphero"""
        snapshot['status'] = snapshot['status'].replace(
            "InventorySnapshotStatus.", "")
        snapshot['created_at_shiphero'] = from_iso(snapshot['created_at'])
        snapshot['updated_at_shiphero'] = from_iso(snapshot['updated_at'])
        del snapshot['created_at']
        del snapshot['updated_at']
        if snapshot['enqueued_at']:
            snapshot['enqueued_at'] = from_iso(snapshot['enqueued_at'])
        if snapshot['snapshot_expiration']:
            snapshot['snapshot_expiration'] = from_iso(
                snapshot['snapshot_expiration'])
        return snapshot

    def create(self, params: InventorySnapshotCreate):
        """Request a new inventory snapshot"""
        try:
            snapshot_raw = self.generate(params)
            snapshot_transformed = self.transform(snapshot_raw)
            snapshot = InventorySnapshot(**snapshot_transformed)
            snapshot.id = generate_id(self.db, 'is', InventorySnapshot)
            snapshot.user_id = self.user.id
            self.db.add(snapshot)
            self.db.commit()
            self.db.refresh(snapshot)
            return snapshot
        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e

    def read(self, db_id: str):
        """Retrieve one snapshot record from database"""
        try:
            snapshot = self.db.query(InventorySnapshot).filter(
                InventorySnapshot.id == db_id).first()
            if not snapshot:
                raise Exception('Snapshot not found')
            return snapshot
        except Exception as e:
            raise Exception(str(e)) from e

    def read_many(self,
                  query: str = None,
                  db_id: str = None,
                  status: str = None,
                  sort_by: str = "created_at",
                  sort_order: str = "desc",
                  page: int = 1,
                  limit: int = 10):
        """Retrieve multiple snapshot records from database"""
        try:
            snapshots = self.db.query(InventorySnapshot)
            pagination = Pagination()
            pagination.total = snapshots.count()
            if db_id:
                snapshots = snapshots.filter(InventorySnapshot.id == db_id)
            if status:
                status = status.split(',')
                snapshots = snapshots.filter(
                    InventorySnapshot.status.in_(status))
            if query:
                query = query.lower()
                searchable_cols = ['customer_account_id',
                                   'created_at',
                                   'updated_at',
                                   'enqueued_at',
                                   'email_error',
                                   'error', 'file_id',
                                   'id',
                                   'job_account_id',
                                   'job_user_id',
                                   'notification_email',
                                   'post_error',
                                   'post_url',
                                   'snapshot_id',
                                   'snapshot_url',
                                   'status',
                                   'user_id',
                                   'warehouse_id']
                snapshots = snapshots.filter(or_(
                    func.lower(getattr(InventorySnapshot, col)).contains(query)
                    for col in searchable_cols))
            sort_field = getattr(InventorySnapshot, sort_by)
            snapshots = snapshots.order_by(
                sort_field.asc() if sort_order == "asc" else sort_field.desc())
            pagination.filtered = snapshots.count()
            snapshots = snapshots.offset((page - 1) * limit).limit(limit).all()
            return snapshots, pagination
        except Exception as e:
            raise Exception(str(e)) from e

    def update(self, db_id: str):
        """Update an inventory snapshot by database id"""
        try:
            snapshot: InventorySnapshot = self.read(db_id)
            snapshot_update_raw = self.extract(snapshot.snapshot_id)
            snapshot_update_transformed = self.transform(snapshot_update_raw)
            for key, value in snapshot_update_transformed.items():
                if hasattr(snapshot, key):
                    setattr(snapshot, key, value)
            self.db.commit()
            self.db.refresh(snapshot)
            return snapshot
        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e
