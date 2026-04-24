from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from users.schemas import *
from users.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from auth.jwt_auth import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)
from core.language import get_language
from core.i18n import translate

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(
    request: UserLoginSchema,
    response: Response,
    db: Session = Depends(get_db),
    lang: str = Depends(get_language),
):
    user_obj: UserModel | None = (
        db.query(UserModel).filter_by(username=request.username.lower()).first()
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=translate(lang, "not_found"),
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=translate(lang, "invalid_user_pass"),
        )

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)

    # access token cookie
    # response.set_cookie(
    #     key="access_token",
    #     value=access_token,
    #     httponly=True,
    #     secure=False,  # For local development
    #     samesite="lax",
    #     max_age=60 * 5,
    # )

    # refresh token cookie
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=False,  # For local development
    #     samesite="lax",
    #     max_age=60 * 60 * 24,
    # )
    return JSONResponse(
        {
            "detail": translate(lang, "login_success"),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/logout")
async def logout(response: Response, lang: str = Depends(get_language)):
    # response.delete_cookie(
    #     key="access_token",
    #     httponly=True,
    #     secure=False,  # For local development
    #     samesite="lax",
    # )
    # response.delete_cookie(
    #     key="refresh_token",
    #     httponly=True,
    #     secure=False,  # For local development
    #     samesite="lax",
    # )
    return {"detail": translate(lang, "logout_success")}


@router.post("/register")
async def user_register(
    request: UserRegisterSchema,
    db: Session = Depends(get_db),
    lang: str = Depends(get_language),
):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=translate(lang, "already_exists"),
        )
    user_obj = UserModel(username=request.username.lower(),
                         person_id=request.person_id)
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return JSONResponse(
        content={"detail": translate(lang, "operation_success")},
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/refresh-token")
async def user_refresh_token(
    request: UserRefreshTokenSchema,
    response: Response,
    lang: str = Depends(get_language),
):
    user_id = decode_refresh_token(request.refresh_token)
    access_token = generate_access_token(user_id)
    # response.set_cookie(
    #     key="access_token",
    #     value=access_token,
    #     httponly=True,
    #     secure=False,  # For local development
    #     samesite="lax",
    #     max_age=60 * 5,
    # )
    return JSONResponse(
        content={
            "access_token_new": access_token,
            "message ": translate(lang, translate(lang, "operation_success")),
        },
        status_code=status.HTTP_200_OK,
    )
