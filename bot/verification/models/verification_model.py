from datetime import datetime
from typing import cast, Literal

VerificationStatus =  Literal["EmailNotFound", "AlreadyVerified", "EmailAlreadyAssigned", "CodeSent"]

class Verification:
    def __init__(self, status: VerificationStatus, email: str, username: str | None = None, code: int | None = None, expires_at: datetime | None = None):
        self.status = status 
        self.email = email
        self.username = username
        self.code = code
        self.expires_at = expires_at


