from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def error_response(e: Exception) -> JSONResponse:
    if isinstance(e, ValueError):
            code, message = status.HTTP_409_CONFLICT, str(e)
    elif isinstance(e, IntegrityError):
          code, message = status.HTTP_409_CONFLICT, "User already exists or required data is missing."
    elif isinstance(e, SQLAlchemyError):
          code, message = status.HTTP_500_INTERNAL_SERVER_ERROR, "A database error occurred. Please try again later."     
    else:
          code, message = status.HTTP_500_INTERNAL_SERVER_ERROR, "An unexpected error occurred. Please try again later."
    
    return JSONResponse(
        status_code=code
        content={
            "success": False
            "message": message
            "data"   : {}
        }
    )