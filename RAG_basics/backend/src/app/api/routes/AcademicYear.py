from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from typing import Annotated
from backend.src.app.db import(models , database )
from api.schema.AcademicYear import academicyear_request, academicyear_response , AcademicYearUpdate
from sqlalchemy.ext.asyncio import AsyncSession
app = APIRouter()


@app.get("/academic_years/{academic_year_id}")
async def get_academic_years(academic_year_id:int , db : Annotated[AsyncSession, Depends(database.get_db)])-> academicyear_response :
    result = await db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id))
    academic_year = result.scalar_one_or_none()
    if not academic_year:
        raise HTTPException(status_code=404, detail="Academic Year not found")
    return academic_year

@app.post("/academic_years/")
async def create_academic_year(posted_data: academicyear_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> academicyear_response:
    result = await db.execute(select(models.AcademicYear).where(models.AcademicYear.name == posted_data.name))
    academic_year = result.scalar_one_or_none()
    if academic_year:
        raise HTTPException(status_code=400, detail="Academic Year already exists")
    new_academic_year = models.AcademicYear(**posted_data.model_dump())
    db.add(new_academic_year)
    await db.commit()
    await db.refresh(new_academic_year)
    return new_academic_year

@app.put("/academic_years/{academic_year_id}")
async def Update_academic_year(updated_data :academicyear_request,db : Annotated[AsyncSession,Depends(database.get_db)],academic_year_id:int)-> academicyear_response:
    result = await db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id))
    academic_year = result.scalar_one_or_none()
    if academic_year : 
        academic_year.name = updated_data.name
        academic_year.starts_on = updated_data.starts_on
        academic_year.ends_on = updated_data.ends_on
        academic_year.is_active = updated_data.is_active
        await db.commit()
        await db.refresh(academic_year)
        return academic_year
    raise HTTPException(status_code=404, detail="Academic Year not found")


@app.patch("/academic_years/{academic_year_id}") 
async def patch_academic_year (modified_data : AcademicYearUpdate,db : Annotated[AsyncSession,Depends(database.get_db)],academic_year_id:int)-> academicyear_response:
    result = await db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id))
    academic_year = result.scalar_one_or_none()
    if academic_year :
        added_data = modified_data.model_dump(exclude_unset=True) 
        for field , value in added_data.items():
            setattr(academic_year,field,value)
        await db.commit()
        await db.refresh(academic_year)
        return academic_year
    raise HTTPException(status_code=404, detail="Academic Year not found")



@app.delete("/academic_years/{academic_year_id}")
async def delete_academic_year(academic_year_id:int , db : Annotated[AsyncSession, Depends(database.get_db)]):
    result = await db.execute(select(models.AcademicYear).where(models.AcademicYear.id == academic_year_id))
    academic_year = result.scalar_one_or_none()
    if academic_year:
        await db.delete(academic_year)
        await db.commit()
        return {"detail": "Academic Year deleted successfully"}
    raise HTTPException(status_code=404, detail="Academic Year not found")
