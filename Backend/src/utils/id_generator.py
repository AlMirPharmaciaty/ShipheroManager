from sqlalchemy.orm import Session


def generate_id(db: Session, prefix: str, model):
    """
    Generate a unique primary key
    """
    last_id = db.query(model.id).order_by(model.id.desc()).first()
    new_key = 1
    if last_id:
        last_key = int(last_id[0][2:])
        new_key = last_key + 1

    return f"{prefix}{new_key:08d}"
