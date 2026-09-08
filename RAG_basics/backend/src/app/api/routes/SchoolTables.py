from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.app.db import database, models
from api.schema import SchoolTables as schema


app = APIRouter()


async def get_by_id(model, item_id: int, db: AsyncSession):
    result = await db.execute(select(model).where(model.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item


async def create_with_unique_check(model, posted_data, unique_fields: tuple[str, ...], db: AsyncSession):
    conditions = [getattr(model, field) == getattr(posted_data, field) for field in unique_fields]
    result = await db.execute(select(model).where(*conditions))
    existing_item = result.scalar_one_or_none()
    if existing_item:
        raise HTTPException(status_code=400, detail=f"{model.__name__} already exists")

    new_item = model(**posted_data.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


async def update_item(model, item_id: int, updated_data, db: AsyncSession):
    item = await get_by_id(model, item_id, db)
    for field, value in updated_data.model_dump().items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


async def patch_item(model, item_id: int, modified_data, db: AsyncSession):
    item = await get_by_id(model, item_id, db)
    for field, value in modified_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


async def delete_item(model, item_id: int, db: AsyncSession):
    item = await get_by_id(model, item_id, db)
    await db.delete(item)
    await db.commit()
    return {"detail": f"{model.__name__} deleted successfully"}


@app.get("/users/{item_id}")
async def get_user(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.user_response:
    return await get_by_id(models.User, item_id, db)


@app.post("/users/")
async def create_user(posted_data: schema.user_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.user_response:
    return await create_with_unique_check(models.User, posted_data, ("username",), db)


@app.get("/terms/{item_id}")
async def get_term(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.term_response:
    return await get_by_id(models.Term, item_id, db)


@app.post("/terms/")
async def create_term(posted_data: schema.term_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.term_response:
    return await create_with_unique_check(models.Term, posted_data, ("academic_year_id", "name"), db)


@app.get("/grade_levels/{item_id}")
async def get_grade_level(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.gradelevel_response:
    return await get_by_id(models.GradeLevel, item_id, db)


@app.post("/grade_levels/")
async def create_grade_level(posted_data: schema.gradelevel_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.gradelevel_response:
    return await create_with_unique_check(models.GradeLevel, posted_data, ("name",), db)


@app.get("/classrooms/{item_id}")
async def get_classroom(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.classroom_response:
    return await get_by_id(models.Classroom, item_id, db)


@app.post("/classrooms/")
async def create_classroom(posted_data: schema.classroom_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.classroom_response:
    return await create_with_unique_check(models.Classroom, posted_data, ("academic_year_id", "grade_level_id", "name"), db)


@app.get("/students/{item_id}")
async def get_student(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.student_response:
    return await get_by_id(models.Student, item_id, db)


@app.post("/students/")
async def create_student(posted_data: schema.student_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.student_response:
    return await create_with_unique_check(models.Student, posted_data, ("student_code",), db)


@app.get("/guardians/{item_id}")
async def get_guardian(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.guardian_response:
    return await get_by_id(models.Guardian, item_id, db)


@app.get("/student_guardians/{item_id}")
async def get_student_guardian(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.studentguardian_response:
    return await get_by_id(models.StudentGuardian, item_id, db)


@app.post("/student_guardians/")
async def create_student_guardian(posted_data: schema.studentguardian_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.studentguardian_response:
    return await create_with_unique_check(models.StudentGuardian, posted_data, ("student_id", "guardian_id"), db)


@app.get("/staff/{item_id}")
async def get_staff(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.staff_response:
    return await get_by_id(models.Staff, item_id, db)


@app.post("/staff/")
async def create_staff(posted_data: schema.staff_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.staff_response:
    return await create_with_unique_check(models.Staff, posted_data, ("employee_code",), db)


@app.get("/teachers/{item_id}")
async def get_teacher(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teacher_response:
    return await get_by_id(models.Teacher, item_id, db)


@app.post("/teachers/")
async def create_teacher(posted_data: schema.teacher_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teacher_response:
    return await create_with_unique_check(models.Teacher, posted_data, ("staff_id",), db)


@app.get("/subjects/{item_id}")
async def get_subject(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.subject_response:
    return await get_by_id(models.Subject, item_id, db)


@app.post("/subjects/")
async def create_subject(posted_data: schema.subject_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.subject_response:
    return await create_with_unique_check(models.Subject, posted_data, ("name",), db)


@app.get("/teacher_subjects/{item_id}")
async def get_teacher_subject(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teachersubject_response:
    return await get_by_id(models.TeacherSubject, item_id, db)


@app.post("/teacher_subjects/")
async def create_teacher_subject(posted_data: schema.teachersubject_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teachersubject_response:
    return await create_with_unique_check(models.TeacherSubject, posted_data, ("teacher_id", "subject_id"), db)


@app.get("/class_subjects/{item_id}")
async def get_class_subject(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.classsubject_response:
    return await get_by_id(models.ClassSubject, item_id, db)


@app.post("/class_subjects/")
async def create_class_subject(posted_data: schema.classsubject_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.classsubject_response:
    return await create_with_unique_check(models.ClassSubject, posted_data, ("classroom_id", "subject_id"), db)


@app.get("/teacher_class_subjects/{item_id}")
async def get_teacher_class_subject(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teacherclasssubject_response:
    return await get_by_id(models.TeacherClassSubject, item_id, db)


@app.post("/teacher_class_subjects/")
async def create_teacher_class_subject(posted_data: schema.teacherclasssubject_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teacherclasssubject_response:
    return await create_with_unique_check(models.TeacherClassSubject, posted_data, ("teacher_id", "classroom_id", "subject_id", "academic_year_id"), db)


@app.get("/periods/{item_id}")
async def get_period(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.period_response:
    return await get_by_id(models.Period, item_id, db)


@app.post("/periods/")
async def create_period(posted_data: schema.period_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.period_response:
    return await create_with_unique_check(models.Period, posted_data, ("name", "starts_at", "ends_at"), db)


@app.get("/timetable_entries/{item_id}")
async def get_timetable_entry(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.timetableentry_response:
    return await get_by_id(models.TimetableEntry, item_id, db)


@app.post("/timetable_entries/")
async def create_timetable_entry(posted_data: schema.timetableentry_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.timetableentry_response:
    return await create_with_unique_check(models.TimetableEntry, posted_data, ("term_id", "classroom_id", "weekday", "period_id"), db)


@app.get("/substitutions/{item_id}")
async def get_substitution(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.substitution_response:
    return await get_by_id(models.Substitution, item_id, db)


@app.post("/substitutions/")
async def create_substitution(posted_data: schema.substitution_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.substitution_response:
    return await create_with_unique_check(models.Substitution, posted_data, ("timetable_entry_id", "substitution_date"), db)


@app.get("/waiting_sessions/{item_id}")
async def get_waiting_session(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.waitingsession_response:
    return await get_by_id(models.WaitingSession, item_id, db)


@app.post("/waiting_sessions/")
async def create_waiting_session(posted_data: schema.waitingsession_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.waitingsession_response:
    return await create_with_unique_check(models.WaitingSession, posted_data, ("classroom_id", "period_id", "session_date"), db)


@app.get("/staff_attendance/{item_id}")
async def get_staff_attendance(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.staffattendance_response:
    return await get_by_id(models.StaffAttendance, item_id, db)


@app.post("/staff_attendance/")
async def create_staff_attendance(posted_data: schema.staffattendance_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.staffattendance_response:
    return await create_with_unique_check(models.StaffAttendance, posted_data, ("staff_id", "attendance_date"), db)


@app.get("/student_attendance/{item_id}")
async def get_student_attendance(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.studentattendance_response:
    return await get_by_id(models.StudentAttendance, item_id, db)


@app.post("/student_attendance/")
async def create_student_attendance(posted_data: schema.studentattendance_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.studentattendance_response:
    return await create_with_unique_check(models.StudentAttendance, posted_data, ("student_id", "attendance_date"), db)


@app.get("/communications/{item_id}")
async def get_communication(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.communication_response:
    return await get_by_id(models.Communication, item_id, db)


@app.get("/announcements/{item_id}")
async def get_announcement(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.announcement_response:
    return await get_by_id(models.Announcement, item_id, db)


@app.get("/reports/{item_id}")
async def get_report(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.report_response:
    return await get_by_id(models.Report, item_id, db)


@app.get("/documents/{item_id}")
async def get_document(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.document_response:
    return await get_by_id(models.Document, item_id, db)


@app.get("/document_chunks/{item_id}")
async def get_document_chunk(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documentchunk_response:
    return await get_by_id(models.DocumentChunk, item_id, db)


@app.post("/document_chunks/")
async def create_document_chunk(posted_data: schema.documentchunk_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documentchunk_response:
    return await create_with_unique_check(models.DocumentChunk, posted_data, ("document_id", "chunk_index"), db)


@app.get("/document_tags/{item_id}")
async def get_document_tag(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documenttag_response:
    return await get_by_id(models.DocumentTag, item_id, db)


@app.post("/document_tags/")
async def create_document_tag(posted_data: schema.documenttag_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documenttag_response:
    return await create_with_unique_check(models.DocumentTag, posted_data, ("name",), db)


@app.get("/document_tag_links/{item_id}")
async def get_document_tag_link(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documenttaglink_response:
    return await get_by_id(models.DocumentTagLink, item_id, db)


@app.post("/document_tag_links/")
async def create_document_tag_link(posted_data: schema.documenttaglink_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documenttaglink_response:
    return await create_with_unique_check(models.DocumentTagLink, posted_data, ("document_id", "tag_id"), db)


@app.get("/chat_sessions/{item_id}")
async def get_chat_session(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.chatsession_response:
    return await get_by_id(models.ChatSession, item_id, db)


@app.get("/chat_messages/{item_id}")
async def get_chat_message(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.chatmessage_response:
    return await get_by_id(models.ChatMessage, item_id, db)


@app.get("/retrieval_logs/{item_id}")
async def get_retrieval_log(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.retrievallog_response:
    return await get_by_id(models.RetrievalLog, item_id, db)


@app.post("/retrieval_logs/")
async def create_retrieval_log(posted_data: schema.retrievallog_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.retrievallog_response:
    return await create_with_unique_check(models.RetrievalLog, posted_data, ("chat_message_id", "document_chunk_id"), db)


@app.put("/users/{item_id}")
async def update_user(item_id: int, updated_data: schema.user_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.user_response:
    return await update_item(models.User, item_id, updated_data, db)


@app.patch("/users/{item_id}")
async def patch_user(item_id: int, modified_data: schema.user_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.user_response:
    return await patch_item(models.User, item_id, modified_data, db)


@app.delete("/users/{item_id}")
async def delete_user(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.User, item_id, db)


@app.put("/terms/{item_id}")
async def update_term(item_id: int, updated_data: schema.term_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.term_response:
    return await update_item(models.Term, item_id, updated_data, db)


@app.patch("/terms/{item_id}")
async def patch_term(item_id: int, modified_data: schema.term_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.term_response:
    return await patch_item(models.Term, item_id, modified_data, db)


@app.delete("/terms/{item_id}")
async def delete_term(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.Term, item_id, db)


@app.put("/grade_levels/{item_id}")
async def update_grade_level(item_id: int, updated_data: schema.gradelevel_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.gradelevel_response:
    return await update_item(models.GradeLevel, item_id, updated_data, db)


@app.patch("/grade_levels/{item_id}")
async def patch_grade_level(item_id: int, modified_data: schema.gradelevel_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.gradelevel_response:
    return await patch_item(models.GradeLevel, item_id, modified_data, db)


@app.delete("/grade_levels/{item_id}")
async def delete_grade_level(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.GradeLevel, item_id, db)


@app.put("/classrooms/{item_id}")
async def update_classroom(item_id: int, updated_data: schema.classroom_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.classroom_response:
    return await update_item(models.Classroom, item_id, updated_data, db)


@app.patch("/classrooms/{item_id}")
async def patch_classroom(item_id: int, modified_data: schema.classroom_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.classroom_response:
    return await patch_item(models.Classroom, item_id, modified_data, db)


@app.delete("/classrooms/{item_id}")
async def delete_classroom(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.Classroom, item_id, db)


@app.put("/students/{item_id}")
async def update_student(item_id: int, updated_data: schema.student_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.student_response:
    return await update_item(models.Student, item_id, updated_data, db)


@app.patch("/students/{item_id}")
async def patch_student(item_id: int, modified_data: schema.student_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.student_response:
    return await patch_item(models.Student, item_id, modified_data, db)


@app.delete("/students/{item_id}")
async def delete_student(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.Student, item_id, db)


@app.put("/student_guardians/{item_id}")
async def update_student_guardian(item_id: int, updated_data: schema.studentguardian_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.studentguardian_response:
    return await update_item(models.StudentGuardian, item_id, updated_data, db)


@app.patch("/student_guardians/{item_id}")
async def patch_student_guardian(item_id: int, modified_data: schema.studentguardian_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.studentguardian_response:
    return await patch_item(models.StudentGuardian, item_id, modified_data, db)


@app.delete("/student_guardians/{item_id}")
async def delete_student_guardian(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.StudentGuardian, item_id, db)


@app.put("/staff/{item_id}")
async def update_staff(item_id: int, updated_data: schema.staff_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.staff_response:
    return await update_item(models.Staff, item_id, updated_data, db)


@app.patch("/staff/{item_id}")
async def patch_staff(item_id: int, modified_data: schema.staff_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.staff_response:
    return await patch_item(models.Staff, item_id, modified_data, db)


@app.delete("/staff/{item_id}")
async def delete_staff(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.Staff, item_id, db)


@app.put("/teachers/{item_id}")
async def update_teacher(item_id: int, updated_data: schema.teacher_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teacher_response:
    return await update_item(models.Teacher, item_id, updated_data, db)


@app.patch("/teachers/{item_id}")
async def patch_teacher(item_id: int, modified_data: schema.teacher_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teacher_response:
    return await patch_item(models.Teacher, item_id, modified_data, db)


@app.delete("/teachers/{item_id}")
async def delete_teacher(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.Teacher, item_id, db)


@app.put("/subjects/{item_id}")
async def update_subject(item_id: int, updated_data: schema.subject_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.subject_response:
    return await update_item(models.Subject, item_id, updated_data, db)


@app.patch("/subjects/{item_id}")
async def patch_subject(item_id: int, modified_data: schema.subject_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.subject_response:
    return await patch_item(models.Subject, item_id, modified_data, db)


@app.delete("/subjects/{item_id}")
async def delete_subject(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.Subject, item_id, db)


@app.put("/teacher_subjects/{item_id}")
async def update_teacher_subject(item_id: int, updated_data: schema.teachersubject_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teachersubject_response:
    return await update_item(models.TeacherSubject, item_id, updated_data, db)


@app.patch("/teacher_subjects/{item_id}")
async def patch_teacher_subject(item_id: int, modified_data: schema.teachersubject_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teachersubject_response:
    return await patch_item(models.TeacherSubject, item_id, modified_data, db)


@app.delete("/teacher_subjects/{item_id}")
async def delete_teacher_subject(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.TeacherSubject, item_id, db)


@app.put("/class_subjects/{item_id}")
async def update_class_subject(item_id: int, updated_data: schema.classsubject_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.classsubject_response:
    return await update_item(models.ClassSubject, item_id, updated_data, db)


@app.patch("/class_subjects/{item_id}")
async def patch_class_subject(item_id: int, modified_data: schema.classsubject_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.classsubject_response:
    return await patch_item(models.ClassSubject, item_id, modified_data, db)


@app.delete("/class_subjects/{item_id}")
async def delete_class_subject(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.ClassSubject, item_id, db)


@app.put("/teacher_class_subjects/{item_id}")
async def update_teacher_class_subject(item_id: int, updated_data: schema.teacherclasssubject_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teacherclasssubject_response:
    return await update_item(models.TeacherClassSubject, item_id, updated_data, db)


@app.patch("/teacher_class_subjects/{item_id}")
async def patch_teacher_class_subject(item_id: int, modified_data: schema.teacherclasssubject_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.teacherclasssubject_response:
    return await patch_item(models.TeacherClassSubject, item_id, modified_data, db)


@app.delete("/teacher_class_subjects/{item_id}")
async def delete_teacher_class_subject(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.TeacherClassSubject, item_id, db)


@app.put("/periods/{item_id}")
async def update_period(item_id: int, updated_data: schema.period_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.period_response:
    return await update_item(models.Period, item_id, updated_data, db)


@app.patch("/periods/{item_id}")
async def patch_period(item_id: int, modified_data: schema.period_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.period_response:
    return await patch_item(models.Period, item_id, modified_data, db)


@app.delete("/periods/{item_id}")
async def delete_period(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.Period, item_id, db)


@app.put("/timetable_entries/{item_id}")
async def update_timetable_entry(item_id: int, updated_data: schema.timetableentry_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.timetableentry_response:
    return await update_item(models.TimetableEntry, item_id, updated_data, db)


@app.patch("/timetable_entries/{item_id}")
async def patch_timetable_entry(item_id: int, modified_data: schema.timetableentry_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.timetableentry_response:
    return await patch_item(models.TimetableEntry, item_id, modified_data, db)


@app.delete("/timetable_entries/{item_id}")
async def delete_timetable_entry(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.TimetableEntry, item_id, db)


@app.put("/substitutions/{item_id}")
async def update_substitution(item_id: int, updated_data: schema.substitution_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.substitution_response:
    return await update_item(models.Substitution, item_id, updated_data, db)


@app.patch("/substitutions/{item_id}")
async def patch_substitution(item_id: int, modified_data: schema.substitution_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.substitution_response:
    return await patch_item(models.Substitution, item_id, modified_data, db)


@app.delete("/substitutions/{item_id}")
async def delete_substitution(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.Substitution, item_id, db)


@app.put("/waiting_sessions/{item_id}")
async def update_waiting_session(item_id: int, updated_data: schema.waitingsession_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.waitingsession_response:
    return await update_item(models.WaitingSession, item_id, updated_data, db)


@app.patch("/waiting_sessions/{item_id}")
async def patch_waiting_session(item_id: int, modified_data: schema.waitingsession_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.waitingsession_response:
    return await patch_item(models.WaitingSession, item_id, modified_data, db)


@app.delete("/waiting_sessions/{item_id}")
async def delete_waiting_session(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.WaitingSession, item_id, db)


@app.put("/staff_attendance/{item_id}")
async def update_staff_attendance(item_id: int, updated_data: schema.staffattendance_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.staffattendance_response:
    return await update_item(models.StaffAttendance, item_id, updated_data, db)


@app.patch("/staff_attendance/{item_id}")
async def patch_staff_attendance(item_id: int, modified_data: schema.staffattendance_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.staffattendance_response:
    return await patch_item(models.StaffAttendance, item_id, modified_data, db)


@app.delete("/staff_attendance/{item_id}")
async def delete_staff_attendance(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.StaffAttendance, item_id, db)


@app.put("/student_attendance/{item_id}")
async def update_student_attendance(item_id: int, updated_data: schema.studentattendance_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.studentattendance_response:
    return await update_item(models.StudentAttendance, item_id, updated_data, db)


@app.patch("/student_attendance/{item_id}")
async def patch_student_attendance(item_id: int, modified_data: schema.studentattendance_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.studentattendance_response:
    return await patch_item(models.StudentAttendance, item_id, modified_data, db)


@app.delete("/student_attendance/{item_id}")
async def delete_student_attendance(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.StudentAttendance, item_id, db)


@app.put("/document_chunks/{item_id}")
async def update_document_chunk(item_id: int, updated_data: schema.documentchunk_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documentchunk_response:
    return await update_item(models.DocumentChunk, item_id, updated_data, db)


@app.patch("/document_chunks/{item_id}")
async def patch_document_chunk(item_id: int, modified_data: schema.documentchunk_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documentchunk_response:
    return await patch_item(models.DocumentChunk, item_id, modified_data, db)


@app.delete("/document_chunks/{item_id}")
async def delete_document_chunk(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.DocumentChunk, item_id, db)


@app.put("/document_tags/{item_id}")
async def update_document_tag(item_id: int, updated_data: schema.documenttag_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documenttag_response:
    return await update_item(models.DocumentTag, item_id, updated_data, db)


@app.patch("/document_tags/{item_id}")
async def patch_document_tag(item_id: int, modified_data: schema.documenttag_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documenttag_response:
    return await patch_item(models.DocumentTag, item_id, modified_data, db)


@app.delete("/document_tags/{item_id}")
async def delete_document_tag(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.DocumentTag, item_id, db)


@app.put("/document_tag_links/{item_id}")
async def update_document_tag_link(item_id: int, updated_data: schema.documenttaglink_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documenttaglink_response:
    return await update_item(models.DocumentTagLink, item_id, updated_data, db)


@app.patch("/document_tag_links/{item_id}")
async def patch_document_tag_link(item_id: int, modified_data: schema.documenttaglink_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.documenttaglink_response:
    return await patch_item(models.DocumentTagLink, item_id, modified_data, db)


@app.delete("/document_tag_links/{item_id}")
async def delete_document_tag_link(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.DocumentTagLink, item_id, db)


@app.put("/retrieval_logs/{item_id}")
async def update_retrieval_log(item_id: int, updated_data: schema.retrievallog_request, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.retrievallog_response:
    return await update_item(models.RetrievalLog, item_id, updated_data, db)


@app.patch("/retrieval_logs/{item_id}")
async def patch_retrieval_log(item_id: int, modified_data: schema.retrievallog_update, db: Annotated[AsyncSession, Depends(database.get_db)]) -> schema.retrievallog_response:
    return await patch_item(models.RetrievalLog, item_id, modified_data, db)


@app.delete("/retrieval_logs/{item_id}")
async def delete_retrieval_log(item_id: int, db: Annotated[AsyncSession, Depends(database.get_db)]):
    return await delete_item(models.RetrievalLog, item_id, db)

