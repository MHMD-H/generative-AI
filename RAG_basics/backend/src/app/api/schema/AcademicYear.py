from datetime import date
from typing import Generic , TypeVar 
from pydantic import BaseModel, ConfigDict, Field 

T = TypeVar("T")
class AcademicYear(BaseModel):
    name: str = Field(description="Name of the academic year", examples=["2023-2024"], min_length=9)


class academicyear_request(AcademicYear):
    starts_on: date = Field(description="Start date of the academic year", examples=["2023-09-01"])
    ends_on: date = Field(description="End date of the academic year", examples=["2024-08-31"])
    is_active: bool = Field(description="Indicates if the academic year is active")


class academicyear_response(academicyear_request):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique identifier for the academic year")

class AcademicYearUpdate(BaseModel): 
    starts_on: date | None = Field(default = None, description="Start date of the academic year", examples=["2023-09-01"])
    name : str | None = Field(default = None , description="Name of the academic year", examples=["2023-2024"], min_length=9)
    ends_on: date | None = Field(default = None, description="End date of the academic year", examples=["2024-08-31"])
    is_active: bool | None = Field(default = None, description="Indicates if the academic year is active")


class PaginatedResponse( BaseModel , Generic[T]) :
    items : list[T] = Field(description="List of items for the current page")
    total : int = Field(description="Total number of items across all pages")
    limit : int = Field(description="Number of items per page")
    skip : int = Field(description="Offset for pagination")
    has_more : bool = Field(description="Indicates if there are more items to fetch")