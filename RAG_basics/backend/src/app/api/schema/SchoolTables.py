from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field


class response_config(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str = Field(description="Unique username")
    email: str | None = Field(default=None, description="User email")
    password_hash: str | None = Field(default=None, description="Hashed password")
    role: str = Field(description="User role")
    is_active: int = Field(default=1, description="Active user flag")


class user_request(UserBase):
    pass


class user_response(UserBase, response_config):
    id: int
    created_at: datetime
    updated_at: datetime


class TermBase(BaseModel):
    academic_year_id: int
    name: str
    starts_on: date
    ends_on: date


class term_request(TermBase):
    pass


class term_response(TermBase, response_config):
    id: int


class GradeLevelBase(BaseModel):
    name: str
    stage: str | None = None
    sort_order: int = 0


class gradelevel_request(GradeLevelBase):
    pass


class gradelevel_response(GradeLevelBase, response_config):
    id: int


class ClassroomBase(BaseModel):
    grade_level_id: int
    name: str
    capacity: int | None = None
    academic_year_id: int


class classroom_request(ClassroomBase):
    pass


class classroom_response(ClassroomBase, response_config):
    id: int


class StudentBase(BaseModel):
    classroom_id: int | None = None
    student_code: str
    full_name: str
    birth_date: date | None = None
    gender: str | None = None
    status: str = "active"
    notes: str | None = None


class student_request(StudentBase):
    pass


class student_response(StudentBase, response_config):
    id: int


class GuardianBase(BaseModel):
    full_name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    notes: str | None = None


class guardian_response(GuardianBase, response_config):
    id: int


class StudentGuardianBase(BaseModel):
    student_id: int
    guardian_id: int
    relationship: str | None = None
    is_primary: int = 0
    can_receive_messages: int = 1


class studentguardian_request(StudentGuardianBase):
    pass


class studentguardian_response(StudentGuardianBase, response_config):
    id: int


class StaffBase(BaseModel):
    user_id: int | None = None
    employee_code: str
    full_name: str
    job_title: str
    department: str | None = None
    phone: str | None = None
    hire_date: date | None = None
    is_active: int = 1


class staff_request(StaffBase):
    pass


class staff_response(StaffBase, response_config):
    id: int


class TeacherBase(BaseModel):
    staff_id: int
    specialization: str | None = None
    max_periods_per_week: int | None = None


class teacher_request(TeacherBase):
    pass


class teacher_response(TeacherBase, response_config):
    id: int


class SubjectBase(BaseModel):
    name: str
    code: str | None = None
    description: str | None = None


class subject_request(SubjectBase):
    pass


class subject_response(SubjectBase, response_config):
    id: int


class TeacherSubjectBase(BaseModel):
    teacher_id: int
    subject_id: int


class teachersubject_request(TeacherSubjectBase):
    pass


class teachersubject_response(TeacherSubjectBase, response_config):
    id: int


class ClassSubjectBase(BaseModel):
    classroom_id: int
    subject_id: int
    weekly_periods: int = 1


class classsubject_request(ClassSubjectBase):
    pass


class classsubject_response(ClassSubjectBase, response_config):
    id: int


class TeacherClassSubjectBase(BaseModel):
    teacher_id: int
    classroom_id: int
    subject_id: int
    academic_year_id: int


class teacherclasssubject_request(TeacherClassSubjectBase):
    pass


class teacherclasssubject_response(TeacherClassSubjectBase, response_config):
    id: int


class PeriodBase(BaseModel):
    name: str
    starts_at: time
    ends_at: time
    sort_order: int = 0


class period_request(PeriodBase):
    pass


class period_response(PeriodBase, response_config):
    id: int


class TimetableEntryBase(BaseModel):
    term_id: int
    classroom_id: int
    teacher_id: int
    subject_id: int
    period_id: int
    weekday: int
    room: str | None = None


class timetableentry_request(TimetableEntryBase):
    pass


class timetableentry_response(TimetableEntryBase, response_config):
    id: int


class SubstitutionBase(BaseModel):
    timetable_entry_id: int
    absent_teacher_id: int
    substitute_teacher_id: int | None = None
    substitute_staff_id: int | None = None
    substitution_date: date
    reason: str | None = None
    status: str = "planned"


class substitution_request(SubstitutionBase):
    pass


class substitution_response(SubstitutionBase, response_config):
    id: int


class WaitingSessionBase(BaseModel):
    substitution_id: int | None = None
    classroom_id: int
    supervisor_staff_id: int | None = None
    period_id: int
    session_date: date
    notes: str | None = None


class waitingsession_request(WaitingSessionBase):
    pass


class waitingsession_response(WaitingSessionBase, response_config):
    id: int


class StaffAttendanceBase(BaseModel):
    staff_id: int
    attendance_date: date
    check_in_at: time | None = None
    check_out_at: time | None = None
    status: str
    notes: str | None = None


class staffattendance_request(StaffAttendanceBase):
    pass


class staffattendance_response(StaffAttendanceBase, response_config):
    id: int


class StudentAttendanceBase(BaseModel):
    student_id: int
    classroom_id: int
    attendance_date: date
    status: str
    notes: str | None = None


class studentattendance_request(StudentAttendanceBase):
    pass


class studentattendance_response(StudentAttendanceBase, response_config):
    id: int


class CommunicationBase(BaseModel):
    guardian_id: int | None = None
    student_id: int | None = None
    created_by_user_id: int | None = None
    channel: str
    subject: str | None = None
    body: str
    follow_up_at: datetime | None = None


class communication_response(CommunicationBase, response_config):
    id: int
    communication_at: datetime


class AnnouncementBase(BaseModel):
    created_by_user_id: int | None = None
    title: str
    body: str
    audience: str
    published_at: datetime | None = None


class announcement_response(AnnouncementBase, response_config):
    id: int
    created_at: datetime


class ReportBase(BaseModel):
    created_by_user_id: int | None = None
    student_id: int | None = None
    teacher_id: int | None = None
    staff_id: int | None = None
    classroom_id: int | None = None
    title: str
    report_type: str
    body: str


class report_response(ReportBase, response_config):
    id: int
    created_at: datetime


class DocumentBase(BaseModel):
    uploaded_by_user_id: int | None = None
    title: str
    document_type: str
    source_path: str | None = None
    source_url: str | None = None
    mime_type: str | None = None
    visibility: str = "internal"
    content_hash: str | None = None


class document_response(DocumentBase, response_config):
    id: int
    created_at: datetime
    updated_at: datetime


class DocumentChunkBase(BaseModel):
    document_id: int
    chunk_index: int
    content: str
    token_count: int | None = None
    embedding_id: str | None = None
    page_number: int | None = None
    metadata_json: str | None = None


class documentchunk_request(DocumentChunkBase):
    pass


class documentchunk_response(DocumentChunkBase, response_config):
    id: int
    created_at: datetime


class DocumentTagBase(BaseModel):
    name: str


class documenttag_request(DocumentTagBase):
    pass


class documenttag_response(DocumentTagBase, response_config):
    id: int


class DocumentTagLinkBase(BaseModel):
    document_id: int
    tag_id: int


class documenttaglink_request(DocumentTagLinkBase):
    pass


class documenttaglink_response(DocumentTagLinkBase, response_config):
    id: int


class ChatSessionBase(BaseModel):
    user_id: int | None = None
    title: str | None = None


class chatsession_response(ChatSessionBase, response_config):
    id: int
    created_at: datetime
    updated_at: datetime


class ChatMessageBase(BaseModel):
    chat_session_id: int
    role: str
    content: str


class chatmessage_response(ChatMessageBase, response_config):
    id: int
    created_at: datetime


class RetrievalLogBase(BaseModel):
    chat_message_id: int
    document_chunk_id: int
    rank: int
    score: float | None = None


class retrievallog_request(RetrievalLogBase):
    pass


class retrievallog_response(RetrievalLogBase, response_config):
    id: int
    created_at: datetime
