from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from typing import Annotated
from DB import(models , database )
from api.schema.AcademicYear import academicyear_request, academicyear_response , AcademicYearUpdate
from sqlalchemy.orm import Session
app = APIRouter()


@app.get("/academic_years/{academic_year_id}")
def get_academic_years(academic_year_id:int , db : Annotated[Session, Depends(database.get_db)])-> academicyear_response :
    academic_year = db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id)).scalar_one_or_none()
    if not academic_year:
        raise HTTPException(status_code=404, detail="Academic Year not found")
    return academic_year

@app.post("/academic_years/")
def create_academic_year(posted_data: academicyear_request, db: Annotated[Session, Depends(database.get_db)]) -> academicyear_response:
    academic_year = db.execute(select(models.AcademicYear).where(models.AcademicYear.name == posted_data.name)).scalar_one_or_none()
    if academic_year:
        raise HTTPException(status_code=400, detail="Academic Year already exists")
    new_academic_year = models.AcademicYear(**posted_data.model_dump())
    db.add(new_academic_year)
    db.commit()
    db.refresh(new_academic_year)
    return new_academic_year

@app.put("/academic_years/{academic_year_id}")
def Update_academic_year(updated_data :academicyear_request,db : Annotated[Session,Depends(database.get_db)],academic_year_id:int)-> academicyear_response:
    academic_year = db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id)).scalar_one_or_none()
    if academic_year : 
        academic_year.name = updated_data.name
        academic_year.starts_on = updated_data.starts_on
        academic_year.ends_on = updated_data.ends_on
        academic_year.is_active = updated_data.is_active
        db.commit()
        db.refresh(academic_year)
        return academic_year
    raise HTTPException(status_code=404, detail="Academic Year not found")


@app.patch("/academic_years/{academic_year_id}") 
def patch_academic_year (modified_data : AcademicYearUpdate,db : Annotated[Session,Depends(database.get_db)],academic_year_id:int)-> academicyear_response:
    academic_year = db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id)).scalar_one_or_none()
    if academic_year :
        added_data = modified_data.model_dump(exclude_unset=True) 
        for field , value in added_data.items():
            setattr(academic_year,field,value)
        db.commit()
        db.refresh(academic_year)
        return academic_year
    raise HTTPException(status_code=404, detail="Academic Year not found")



@app.delete("/academic_years/{academic_year_id}")
def delete_academic_year(academic_year_id:int , db : Annotated[Session, Depends(database.get_db)]):
    academic_year = db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id)).scalar_one_or_none()
    if academic_year:
        db.delete(academic_year)
        db.commit()
        return {"detail": "Academic Year deleted successfully"}
    raise HTTPException(status_code=404, detail="Academic Year not found")
