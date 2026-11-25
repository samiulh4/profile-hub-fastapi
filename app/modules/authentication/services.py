from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.authentication.schemas import SignUpRequest
from app.modules.user.models import User

DEFAULT_USER_TYPE = "USER"
DEFAULT_USER_STATUS = 0


def sign_up(db: Session, signup_request: SignUpRequest) -> User:
    """Create a user. Raises ValueError if identity or e-mail already exists."""
    if db.query(User).filter(User.user_identity == signup_request.user_identity).first():
        raise ValueError("User with this identity already registered.")

    if db.query(User).filter(User.user_email == signup_request.user_email).first():
        raise ValueError("User with this e-mail already registered.")

    now = datetime.now(timezone.utc)

    user = User(
        user_identity=signup_request.user_identity,
        user_full_name=signup_request.user_full_name,
        user_email=signup_request.user_email,
        user_mobile=signup_request.user_mobile,
        user_gender=signup_request.user_gender,
        user_birthday=signup_request.user_birthday,
        user_status=DEFAULT_USER_STATUS,
        user_password=hash_password(signup_request.user_password),
        user_type=DEFAULT_USER_TYPE,
        created_at=now,
        updated_at=now,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
