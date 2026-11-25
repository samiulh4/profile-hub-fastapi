import logging

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.authentication import services
from app.modules.authentication.schemas import SignUpRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "data": {}},
    )


@router.post("/sign-up")
async def sign_up(signup_request: SignUpRequest, db: Session = Depends(get_db)):
    try:
        services.sign_up(db, signup_request)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "User registered successfully.",
                "data": {},
            },
        )
    except ValueError as e:
        return _error_response(status.HTTP_409_CONFLICT, str(e))
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
