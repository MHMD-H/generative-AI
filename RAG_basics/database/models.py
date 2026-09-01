from __future__ import annotations

from datetime import date, datetime, time

from sqlalchemy import CheckConstraint, Date, DateTime, Float, ForeignKey, Index, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'manager', 'teacher', 'staff')"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str | None] = mapped_column(unique=True)
    password_hash: Mapped[str | None] = mapped_column()
    role: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[int] = mapped_column(nullable=False, server_default=text("1"))
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class AcademicYear(Base):
    __tablename__ = "academic_years"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    starts_on: Mapped[date] = mapped_column(Date, nullable=False)
    ends_on: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[int] = mapped_column(nullable=False, server_default=text("0"))


class Term(Base):
    __tablename__ = "terms"
    __table_args__ = (
        UniqueConstraint("academic_year_id", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    academic_year_id: Mapped[int] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    starts_on: Mapped[date] = mapped_column(Date, nullable=False)
    ends_on: Mapped[date] = mapped_column(Date, nullable=False)


class GradeLevel(Base):
    __tablename__ = "grade_levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    stage: Mapped[str | None] = mapped_column()
    sort_order: Mapped[int] = mapped_column(nullable=False, server_default=text("0"))


class Classroom(Base):
    __tablename__ = "classrooms"
    __table_args__ = (
        UniqueConstraint("academic_year_id", "grade_level_id", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    grade_level_id: Mapped[int] = mapped_column(ForeignKey("grade_levels.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    capacity: Mapped[int | None] = mapped_column()
    academic_year_id: Mapped[int] = mapped_column(ForeignKey("academic_years.id"), nullable=False)


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (
        CheckConstraint("gender IN ('male', 'female')"),
        CheckConstraint("status IN ('active', 'inactive', 'graduated', 'transferred')"),
        Index("idx_students_classroom_id", "classroom_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int | None] = mapped_column(ForeignKey("classrooms.id", ondelete="SET NULL"))
    student_code: Mapped[str] = mapped_column(nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date)
    gender: Mapped[str | None] = mapped_column()
    status: Mapped[str] = mapped_column(nullable=False, server_default=text("'active'"))
    notes: Mapped[str | None] = mapped_column(Text)


class Guardian(Base):
    __tablename__ = "guardians"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str | None] = mapped_column()
    email: Mapped[str | None] = mapped_column()
    address: Mapped[str | None] = mapped_column()
    notes: Mapped[str | None] = mapped_column(Text)


class StudentGuardian(Base):
    __tablename__ = "student_guardians"
    __table_args__ = (
        UniqueConstraint("student_id", "guardian_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    guardian_id: Mapped[int] = mapped_column(ForeignKey("guardians.id", ondelete="CASCADE"), nullable=False)
    relationship: Mapped[str | None] = mapped_column()
    is_primary: Mapped[int] = mapped_column(nullable=False, server_default=text("0"))
    can_receive_messages: Mapped[int] = mapped_column(nullable=False, server_default=text("1"))


class Staff(Base):
    __tablename__ = "staff"
    __table_args__ = (
        Index("idx_staff_job_title", "job_title"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), unique=True)
    employee_code: Mapped[str] = mapped_column(nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    job_title: Mapped[str] = mapped_column(nullable=False)
    department: Mapped[str | None] = mapped_column()
    phone: Mapped[str | None] = mapped_column()
    hire_date: Mapped[date | None] = mapped_column(Date)
    is_active: Mapped[int] = mapped_column(nullable=False, server_default=text("1"))


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, unique=True)
    specialization: Mapped[str | None] = mapped_column()
    max_periods_per_week: Mapped[int | None] = mapped_column()


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    code: Mapped[str | None] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(Text)


class TeacherSubject(Base):
    __tablename__ = "teacher_subjects"
    __table_args__ = (
        UniqueConstraint("teacher_id", "subject_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)


class ClassSubject(Base):
    __tablename__ = "class_subjects"
    __table_args__ = (
        UniqueConstraint("classroom_id", "subject_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    weekly_periods: Mapped[int] = mapped_column(nullable=False, server_default=text("1"))


class TeacherClassSubject(Base):
    __tablename__ = "teacher_class_subjects"
    __table_args__ = (
        UniqueConstraint("teacher_id", "classroom_id", "subject_id", "academic_year_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    academic_year_id: Mapped[int] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)


class Period(Base):
    __tablename__ = "periods"
    __table_args__ = (
        UniqueConstraint("name", "starts_at", "ends_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    starts_at: Mapped[time] = mapped_column(nullable=False)
    ends_at: Mapped[time] = mapped_column(nullable=False)
    sort_order: Mapped[int] = mapped_column(nullable=False, server_default=text("0"))


class TimetableEntry(Base):
    __tablename__ = "timetable_entries"
    __table_args__ = (
        CheckConstraint("weekday BETWEEN 0 AND 6"),
        UniqueConstraint("term_id", "classroom_id", "weekday", "period_id"),
        UniqueConstraint("term_id", "teacher_id", "weekday", "period_id"),
        Index("idx_timetable_lookup", "term_id", "weekday", "period_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    term_id: Mapped[int] = mapped_column(ForeignKey("terms.id", ondelete="CASCADE"), nullable=False)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("periods.id", ondelete="CASCADE"), nullable=False)
    weekday: Mapped[int] = mapped_column(nullable=False)
    room: Mapped[str | None] = mapped_column()


class Substitution(Base):
    __tablename__ = "substitutions"
    __table_args__ = (
        CheckConstraint("status IN ('planned', 'completed', 'cancelled')"),
        UniqueConstraint("timetable_entry_id", "substitution_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    timetable_entry_id: Mapped[int] = mapped_column(ForeignKey("timetable_entries.id", ondelete="CASCADE"), nullable=False)
    absent_teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    substitute_teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"))
    substitute_staff_id: Mapped[int | None] = mapped_column(ForeignKey("staff.id"))
    substitution_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(nullable=False, server_default=text("'planned'"))


class WaitingSession(Base):
    __tablename__ = "waiting_sessions"
    __table_args__ = (
        UniqueConstraint("classroom_id", "period_id", "session_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    substitution_id: Mapped[int | None] = mapped_column(ForeignKey("substitutions.id", ondelete="SET NULL"))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    supervisor_staff_id: Mapped[int | None] = mapped_column(ForeignKey("staff.id", ondelete="SET NULL"))
    period_id: Mapped[int] = mapped_column(ForeignKey("periods.id", ondelete="CASCADE"), nullable=False)
    session_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)


class StaffAttendance(Base):
    __tablename__ = "staff_attendance"
    __table_args__ = (
        CheckConstraint("status IN ('present', 'absent', 'late', 'excused')"),
        UniqueConstraint("staff_id", "attendance_date"),
        Index("idx_staff_attendance_date", "attendance_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)
    check_in_at: Mapped[time | None] = mapped_column()
    check_out_at: Mapped[time | None] = mapped_column()
    status: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)


class StudentAttendance(Base):
    __tablename__ = "student_attendance"
    __table_args__ = (
        CheckConstraint("status IN ('present', 'absent', 'late', 'excused')"),
        UniqueConstraint("student_id", "attendance_date"),
        Index("idx_student_attendance_date", "attendance_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)


class Communication(Base):
    __tablename__ = "communications"
    __table_args__ = (
        CheckConstraint("channel IN ('phone', 'sms', 'whatsapp', 'email', 'meeting', 'note')"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    guardian_id: Mapped[int | None] = mapped_column(ForeignKey("guardians.id", ondelete="SET NULL"))
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id", ondelete="SET NULL"))
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    channel: Mapped[str] = mapped_column(nullable=False)
    subject: Mapped[str | None] = mapped_column()
    body: Mapped[str] = mapped_column(Text, nullable=False)
    communication_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    follow_up_at: Mapped[datetime | None] = mapped_column(DateTime)


class Announcement(Base):
    __tablename__ = "announcements"
    __table_args__ = (
        CheckConstraint("audience IN ('all', 'teachers', 'staff', 'guardians', 'students')"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    audience: Mapped[str] = mapped_column(nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id", ondelete="SET NULL"))
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id", ondelete="SET NULL"))
    staff_id: Mapped[int | None] = mapped_column(ForeignKey("staff.id", ondelete="SET NULL"))
    classroom_id: Mapped[int | None] = mapped_column(ForeignKey("classrooms.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(nullable=False)
    report_type: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint("visibility IN ('public', 'internal', 'private')"),
        Index("idx_documents_type", "document_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    uploaded_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(nullable=False)
    document_type: Mapped[str] = mapped_column(nullable=False)
    source_path: Mapped[str | None] = mapped_column()
    source_url: Mapped[str | None] = mapped_column()
    mime_type: Mapped[str | None] = mapped_column()
    visibility: Mapped[str] = mapped_column(nullable=False, server_default=text("'internal'"))
    content_hash: Mapped[str | None] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index"),
        Index("idx_document_chunks_document_id", "document_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None] = mapped_column()
    embedding_id: Mapped[str | None] = mapped_column()
    page_number: Mapped[int | None] = mapped_column()
    metadata_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class DocumentTag(Base):
    __tablename__ = "document_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class DocumentTagLink(Base):
    __tablename__ = "document_tag_links"
    __table_args__ = (
        UniqueConstraint("document_id", "tag_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey("document_tags.id", ondelete="CASCADE"), nullable=False)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    title: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant', 'system')"),
        Index("idx_chat_messages_session_id", "chat_session_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"
    __table_args__ = (
        UniqueConstraint("chat_message_id", "document_chunk_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_message_id: Mapped[int] = mapped_column(ForeignKey("chat_messages.id", ondelete="CASCADE"), nullable=False)
    document_chunk_id: Mapped[int] = mapped_column(ForeignKey("document_chunks.id", ondelete="CASCADE"), nullable=False)
    rank: Mapped[int] = mapped_column(nullable=False)
    score: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("CURRENT_TIMESTAMP"))
