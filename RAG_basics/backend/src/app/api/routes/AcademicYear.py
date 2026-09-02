from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from typing import Annotated
from DB import(models , database )
from api.schema.AcademicYear import academicyear_request, academicyear_response
from sqlalchemy.orm import Session
app = APIRouter()


@app.get("/academic_years/{academic_year_id}")
def get_academic_years(academic_year_id:int , db : Annotated[Session, Depends(database.get_db)])-> academicyear_response :
    academic_year = db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id)).scalar_one_or_none()
    if not academic_year:
        raise HTTPException(status_code=404, detail="Academic Year not found")
    return academic_year

@app.post("/academic_years/")
def create_academicyear(posted_data: academicyear_request, db: Annotated[Session, Depends(database.get_db)]) -> academicyear_response:
    academic_year = db.execute(select(models.AcademicYear).where(models.AcademicYear.name == posted_data.name)).scalar_one_or_none()
    if academic_year:
        raise HTTPException(status_code=400, detail="Academic Year already exists")
    new_academic_year = models.AcademicYear(**posted_data.model_dump())
    db.add(new_academic_year)
    db.commit()
    db.refresh(new_academic_year)
    return new_academic_year
