from sqlalchemy.orm import Session

from src.utils.id_generator import generate_id
from src.schemas.enums import ETLLogProcessessEnum
from src.models.user_models.user import User
from src.models.etl_log import ETLLog


class ETLLogController:
    """
    Shiphero ELT log controller
    """

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def create_log(self,
                   process: ETLLogProcessessEnum,
                   success: bool,
                   description: str,
                   file_id: str | None = None):
        """"""
        try:
            log = ETLLog()
            log.id = generate_id(self.db, 'll', ETLLog)
            log.user_id = self.user.id
            log.process = process
            log.success = success
            log.description = description
            log.file_id = file_id
            self.db.add(log)
            self.db.commit()
            self.db.refresh(log)
            return log
        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e
