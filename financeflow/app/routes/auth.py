from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.services.auth_service import (
    create_access_token,
    create_refresh_token,
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_id,
    verify_refresh_token,
    verify_token,
)

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr


@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest):
    existing_user = get_user_by_email(data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    user_id = create_user(data.email, data.password)
    access_token = create_access_token({"sub": str(user_id), "email": data.email})
    refresh_token = create_refresh_token({"sub": str(user_id), "email": data.email})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    user = authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    access_token = create_access_token({"sub": str(user["id"]), "email": user["email"]})
    refresh_token = create_refresh_token({"sub": str(user["id"]), "email": user["email"]})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshRequest):
    payload = verify_refresh_token(data.refresh_token)
    user_id = int(payload["sub"])
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    access_token = create_access_token({"sub": str(user_id), "email": user["email"]})
    refresh_token = create_refresh_token({"sub": str(user_id), "email": user["email"]})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserResponse)
async def read_current_user(user_id: str = Depends(verify_token)):
    user = get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserResponse(user_id=int(user_id), email=user["email"])
