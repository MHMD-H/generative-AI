from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from DB import database, models
from api.schema import SchoolTables as schema


app = APIRouter()


def get_by_id(model, item_id: int, db: Session):
    item = db.execute(select(model).where(model.id == item_id)).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item


def create_with_unique_check(model, posted_data, unique_fields: tuple[str, ...], db: Session):
    conditions = [getattr(model, field) == getattr(posted_data, field) for field in unique_fields]
    existing_item = db.execute(select(model).where(*conditions)).scalar_one_or_none()
    if existing_item:
        raise HTTPException(status_code=400, detail=f"{model.__name__} already exists")

    new_item = model(**posted_data.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/users/{item_id}")
def get_user(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.user_response:
    return get_by_id(models.User, item_id, db)


@app.post("/users/")
def create_user(posted_data: schema.user_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.user_response:
    return create_with_unique_check(models.User, posted_data, ("username",), db)


@app.get("/terms/{item_id}")
def get_term(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.term_response:
    return get_by_id(models.Term, item_id, db)


@app.post("/terms/")
def create_term(posted_data: schema.term_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.term_response:
    return create_with_unique_check(models.Term, posted_data, ("academic_year_id", "name"), db)


@app.get("/grade_levels/{item_id}")
def get_grade_level(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.gradelevel_response:
    return get_by_id(models.GradeLevel, item_id, db)


@app.post("/grade_levels/")
def create_grade_level(posted_data: schema.gradelevel_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.gradelevel_response:
    return create_with_unique_check(models.GradeLevel, posted_data, ("name",), db)


@app.get("/classrooms/{item_id}")
def get_classroom(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.classroom_response:
    return get_by_id(models.Classroom, item_id, db)


@app.post("/classrooms/")
def create_classroom(posted_data: schema.classroom_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.classroom_response:
    return create_with_unique_check(models.Classroom, posted_data, ("academic_year_id", "grade_level_id", "name"), db)


@app.get("/students/{item_id}")
def get_student(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.student_response:
    return get_by_id(models.Student, item_id, db)


@app.post("/students/")
def create_student(posted_data: schema.student_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.student_response:
    return create_with_unique_check(models.Student, posted_data, ("student_code",), db)


@app.get("/guardians/{item_id}")
def get_guardian(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.guardian_response:
    return get_by_id(models.Guardian, item_id, db)


@app.get("/student_guardians/{item_id}")
def get_student_guardian(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.studentguardian_response:
    return get_by_id(models.StudentGuardian, item_id, db)


@app.post("/student_guardians/")
def create_student_guardian(posted_data: schema.studentguardian_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.studentguardian_response:
    return create_with_unique_check(models.StudentGuardian, posted_data, ("student_id", "guardian_id"), db)


@app.get("/staff/{item_id}")
def get_staff(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.staff_response:
    return get_by_id(models.Staff, item_id, db)


@app.post("/staff/")
def create_staff(posted_data: schema.staff_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.staff_response:
    return create_with_unique_check(models.Staff, posted_data, ("employee_code",), db)


@app.get("/teachers/{item_id}")
def get_teacher(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.teacher_response:
    return get_by_id(models.Teacher, item_id, db)


@app.post("/teachers/")
def create_teacher(posted_data: schema.teacher_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.teacher_response:
    return create_with_unique_check(models.Teacher, posted_data, ("staff_id",), db)


@app.get("/subjects/{item_id}")
def get_subject(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.subject_response:
    return get_by_id(models.Subject, item_id, db)


@app.post("/subjects/")
def create_subject(posted_data: schema.subject_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.subject_response:
    return create_with_unique_check(models.Subject, posted_data, ("name",), db)


@app.get("/teacher_subjects/{item_id}")
def get_teacher_subject(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.teachersubject_response:
    return get_by_id(models.TeacherSubject, item_id, db)


@app.post("/teacher_subjects/")
def create_teacher_subject(posted_data: schema.teachersubject_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.teachersubject_response:
    return create_with_unique_check(models.TeacherSubject, posted_data, ("teacher_id", "subject_id"), db)


@app.get("/class_subjects/{item_id}")
def get_class_subject(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.classsubject_response:
    return get_by_id(models.ClassSubject, item_id, db)


@app.post("/class_subjects/")
def create_class_subject(posted_data: schema.classsubject_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.classsubject_response:
    return create_with_unique_check(models.ClassSubject, posted_data, ("classroom_id", "subject_id"), db)


@app.get("/teacher_class_subjects/{item_id}")
def get_teacher_class_subject(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.teacherclasssubject_response:
    return get_by_id(models.TeacherClassSubject, item_id, db)


@app.post("/teacher_class_subjects/")
def create_teacher_class_subject(posted_data: schema.teacherclasssubject_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.teacherclasssubject_response:
    return create_with_unique_check(models.TeacherClassSubject, posted_data, ("teacher_id", "classroom_id", "subject_id", "academic_year_id"), db)


@app.get("/periods/{item_id}")
def get_period(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.period_response:
    return get_by_id(models.Period, item_id, db)


@app.post("/periods/")
def create_period(posted_data: schema.period_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.period_response:
    return create_with_unique_check(models.Period, posted_data, ("name", "starts_at", "ends_at"), db)


@app.get("/timetable_entries/{item_id}")
def get_timetable_entry(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.timetableentry_response:
    return get_by_id(models.TimetableEntry, item_id, db)


@app.post("/timetable_entries/")
def create_timetable_entry(posted_data: schema.timetableentry_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.timetableentry_response:
    return create_with_unique_check(models.TimetableEntry, posted_data, ("term_id", "classroom_id", "weekday", "period_id"), db)


@app.get("/substitutions/{item_id}")
def get_substitution(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.substitution_response:
    return get_by_id(models.Substitution, item_id, db)


@app.post("/substitutions/")
def create_substitution(posted_data: schema.substitution_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.substitution_response:
    return create_with_unique_check(models.Substitution, posted_data, ("timetable_entry_id", "substitution_date"), db)


@app.get("/waiting_sessions/{item_id}")
def get_waiting_session(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.waitingsession_response:
    return get_by_id(models.WaitingSession, item_id, db)


@app.post("/waiting_sessions/")
def create_waiting_session(posted_data: schema.waitingsession_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.waitingsession_response:
    return create_with_unique_check(models.WaitingSession, posted_data, ("classroom_id", "period_id", "session_date"), db)


@app.get("/staff_attendance/{item_id}")
def get_staff_attendance(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.staffattendance_response:
    return get_by_id(models.StaffAttendance, item_id, db)


@app.post("/staff_attendance/")
def create_staff_attendance(posted_data: schema.staffattendance_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.staffattendance_response:
    return create_with_unique_check(models.StaffAttendance, posted_data, ("staff_id", "attendance_date"), db)


@app.get("/student_attendance/{item_id}")
def get_student_attendance(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.studentattendance_response:
    return get_by_id(models.StudentAttendance, item_id, db)


@app.post("/student_attendance/")
def create_student_attendance(posted_data: schema.studentattendance_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.studentattendance_response:
    return create_with_unique_check(models.StudentAttendance, posted_data, ("student_id", "attendance_date"), db)


@app.get("/communications/{item_id}")
def get_communication(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.communication_response:
    return get_by_id(models.Communication, item_id, db)


@app.get("/announcements/{item_id}")
def get_announcement(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.announcement_response:
    return get_by_id(models.Announcement, item_id, db)


@app.get("/reports/{item_id}")
def get_report(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.report_response:
    return get_by_id(models.Report, item_id, db)


@app.get("/documents/{item_id}")
def get_document(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.document_response:
    return get_by_id(models.Document, item_id, db)


@app.get("/document_chunks/{item_id}")
def get_document_chunk(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.documentchunk_response:
    return get_by_id(models.DocumentChunk, item_id, db)


@app.post("/document_chunks/")
def create_document_chunk(posted_data: schema.documentchunk_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.documentchunk_response:
    return create_with_unique_check(models.DocumentChunk, posted_data, ("document_id", "chunk_index"), db)


@app.get("/document_tags/{item_id}")
def get_document_tag(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.documenttag_response:
    return get_by_id(models.DocumentTag, item_id, db)


@app.post("/document_tags/")
def create_document_tag(posted_data: schema.documenttag_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.documenttag_response:
    return create_with_unique_check(models.DocumentTag, posted_data, ("name",), db)


@app.get("/document_tag_links/{item_id}")
def get_document_tag_link(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.documenttaglink_response:
    return get_by_id(models.DocumentTagLink, item_id, db)


@app.post("/document_tag_links/")
def create_document_tag_link(posted_data: schema.documenttaglink_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.documenttaglink_response:
    return create_with_unique_check(models.DocumentTagLink, posted_data, ("document_id", "tag_id"), db)


@app.get("/chat_sessions/{item_id}")
def get_chat_session(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.chatsession_response:
    return get_by_id(models.ChatSession, item_id, db)


@app.get("/chat_messages/{item_id}")
def get_chat_message(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.chatmessage_response:
    return get_by_id(models.ChatMessage, item_id, db)


@app.get("/retrieval_logs/{item_id}")
def get_retrieval_log(item_id: int, db: Annotated[Session, Depends(database.get_db)]) -> schema.retrievallog_response:
    return get_by_id(models.RetrievalLog, item_id, db)


@app.post("/retrieval_logs/")
def create_retrieval_log(posted_data: schema.retrievallog_request, db: Annotated[Session, Depends(database.get_db)]) -> schema.retrievallog_response:
    return create_with_unique_check(models.RetrievalLog, posted_data, ("chat_message_id", "document_chunk_id"), db)
