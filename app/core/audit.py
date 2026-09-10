from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def log_action(db: Session, action: str, detail: str = "", user_id: int | None = None):
    entry = AuditLog(user_id=user_id, action=action, detail=detail)
    db.add(entry)