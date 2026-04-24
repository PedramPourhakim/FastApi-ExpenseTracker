from fastapi import APIRouter, Path, HTTPException, status, Query, Depends
from typing import List
from expenses.schemas import *
from core.database import get_db
from sqlalchemy.orm import Session
from expenses.models import ExpenseModel
from fastapi.responses import JSONResponse
from users.models import UserModel
from auth.jwt_auth import get_current_user
from core.language import get_language
from core.i18n import translate
import logging

from fastapi_cache.decorator import cache

router = APIRouter(tags=["Expenses"], prefix="/expenses")

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@cache(expire=10)
@router.get(
    "",
    response_model=List[ResponseExpenseSchema],
    status_code=status.HTTP_200_OK,
)
def retrieve_expenses(
    q: str | None = Query(
        alias="search",
        description="Search all expenses by their description",
        default=None,
        max_length=50,
    ),
    limit: int = Query(
        default=10,
        gt=0,
        le=50,
        description="limiting the number of items to retrieve",
    ),
    offset: int = Query(
        default=0, ge=0, description="use for pagination based on passed items"
    ),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    query = db.query(ExpenseModel).filter_by(person_id=user.person_id)
    if q:
        query = query.filter_by(description=q)
    return query.limit(limit).offset(offset).all()



@router.get(
    "/{expense_id}",
    response_model=ResponseExpenseSchema,
    status_code=status.HTTP_200_OK,
)
def retrieve_expense(
    expense_id: str = Path(..., description="id of the expense"),
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
    lang: str = Depends(get_language),
):
    expense_obj = (
        db.query(ExpenseModel)
        .filter_by(person_id=user.person_id, id=expense_id)
        .first()
    )
    if not expense_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=translate(lang, "not_found"),
        )
    else:
        return expense_obj


@router.post(
    "",
    response_model=ResponseExpenseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    request: CreateExpenseSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    data = request.model_dump()
    data.update({"person_id": user.person_id})
    # logger.info(f"Person Id: {user.person_id}")
    # logger.info(f"data: {data}")
    expense_obj = ExpenseModel(**data)
    db.add(expense_obj)
    db.commit()
    db.refresh(expense_obj)
    return expense_obj


@router.put(
    "/{expense_id}",
    response_model=ResponseExpenseSchema,
    status_code=status.HTTP_200_OK,
)
def update_expense(
    request: UpdateExpenseSchema,
    expense_id: str = Path(..., description="id of the expense"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
    lang: str = Depends(get_language),
):
    expense_obj = (
        db.query(ExpenseModel)
        .filter_by(id=expense_id, person_id=user.person_id)
        .first()
    )
    if expense_obj:
        for field, value in request.model_dump(exclude_unset=True).items():
            setattr(expense_obj, field, value)
        db.commit()
        db.refresh(expense_obj)
        return expense_obj
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=translate(lang, "not_found"),
        )


@router.delete(
    "/{expense_id}",
    response_model=ResponseExpenseSchema,
    status_code=status.HTTP_200_OK,
)
def delete_expense(
    expense_id: str = Path(..., description="id of the expense"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
    lang: str = Depends(get_language),
):
    expense_obj = (
        db.query(ExpenseModel)
        .filter_by(person_id=user.person_id, id=expense_id)
        .one_or_none()
    )
    if expense_obj:
        db.delete(expense_obj)
        db.commit()
        return JSONResponse(
            content={"detail": "object removed successfully"},
            status_code=status.HTTP_200_OK,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=translate(lang, "not_found"),
        )
