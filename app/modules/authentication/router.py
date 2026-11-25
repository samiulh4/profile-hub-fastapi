from fastapi import APIRouter, Depends, status, HTTPException, Header

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/sign-up")
async def sign_up():
    return {"message": "Sign up endpoint"}