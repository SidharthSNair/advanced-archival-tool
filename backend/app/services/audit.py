import json
from app.models import AuditLog

def audit_log(db, action: str, user_ip: str | None, details: dict | None = None):
    entry = AuditLog(action=action, user_ip=user_ip, details=json.dumps(details or {}))
    db.add(entry); db.commit()
