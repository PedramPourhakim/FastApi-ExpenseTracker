from fastapi import APIRouter, Path, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from people.schemas import *
from people.models import *
from core.database import get_db
from core.language import get_language
from core.i18n import translate
from fastapi_cache.decorator import cache


router = APIRouter(tags=["People"], prefix="/people")

@cache(expire=5)
@router.get(
    "/people",
    status_code=status.HTTP_200_OK,
    response_model=List[ResponsePersonSchema],
)
def retrieve_all_people(
    q: str | None = Query(
        alias="search",
        description="Search all people by their firstname",
        default=None,
        max_length=50,
    ),
    db: Session = Depends(get_db),
):
    query = db.query(PersonModel)
    if q:
        query = query.filter_by(first_name=q)
    get_all_query_result = query.all()
    return get_all_query_result


@router.get(
    "/people/{person_id}",
    response_model=ResponsePersonSchema,
    status_code=status.HTTP_200_OK,
)
def retrieve_person(
    person_id: str = Path(..., description="id of the person"),
    db: Session = Depends(get_db),
    lang: str = Depends(get_language),
):

    person = db.query(PersonModel).filter_by(id=person_id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=translate(lang, "not_found"),
        )


@router.post(
    "/people",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponsePersonSchema,
)
def create_person(request: CreatePersonSchema, db: Session = Depends(get_db)):
    new_person = PersonModel(first_name=request.first_name, last_name=request.last_name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


@router.put(
    "/people/{person_id}",
    response_model=ResponsePersonSchema,
    status_code=status.HTTP_200_OK,
)
def update_person(
    request: UpdatePersonSchema,
    person_id: str = Path(..., description="id of the person"),
    db: Session = Depends(get_db),
    lang: str = Depends(get_language),
):
    person = db.query(PersonModel).filter_by(id=person_id).one_or_none()
    if person:
        person.first_name = request.first_name
        person.last_name = request.last_name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=translate(lang, "not_found"),
        )


@router.delete("/people/{person_id}")
def delete_person(
    person_id: str,
    db: Session = Depends(get_db),
    lang: str = Depends(get_language),
):
    person = db.query(PersonModel).filter_by(id=person_id).one_or_none()
    if person:
        db.delete(person)
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
