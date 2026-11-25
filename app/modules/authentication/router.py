import logging

from fastapi import APIRouter, Depends, status, HTTPException, Header
from app.modules.authentication.schemas import SignUpRequest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.user.models import User
from datetime import datetime, timezone
from app.core.security import hash_password
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

DEFAULT_USER_TYPE = "USER"
DEFAULT_USER_STATUS = 0


def _error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "data": {}},
    )


@router.post("/sign-up")
async def sign_up(signup_request: SignUpRequest, db: Session = Depends(get_db)):
    try:
        existing_identity = (
            db.query(User)
            .filter(User.user_identity == signup_request.user_identity)
            .first()
        )
        if existing_identity:
            return _error_response(
                status.HTTP_409_CONFLICT,
                "User with this identity already registered.",
            )

        existing_email = (
            db.query(User)
            .filter(User.user_email == signup_request.user_email)
            .first()
        )
        if existing_email:
            return _error_response(
                status.HTTP_409_CONFLICT,
                "User with this e-mail already registered.",
            )

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

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "User registered successfully.",
                "data": {},
            },
        )

    except IntegrityError:
        db.rollback()
        logger.exception("Sign-up integrity error")
        return _error_response(
            status.HTTP_409_CONFLICT,
            "User already exists or required data is missing.",
        )
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Sign-up database error")
        return _error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "A database error occurred. Please try again later.",
        )
    except Exception:
        db.rollback()
        logger.exception("Sign-up unexpected error")
        return _error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred. Please try again later.",
        )
