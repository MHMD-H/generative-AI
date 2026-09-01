PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT,
    role TEXT NOT NULL CHECK (role IN ('admin', 'manager', 'teacher', 'staff')),
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS academic_years (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    starts_on TEXT NOT NULL,
    ends_on TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    academic_year_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    starts_on TEXT NOT NULL,
    ends_on TEXT NOT NULL,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years (id) ON DELETE CASCADE,
    UNIQUE (academic_year_id, name)
);

CREATE TABLE IF NOT EXISTS grade_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    stage TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade_level_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    capacity INTEGER,
    academic_year_id INTEGER NOT NULL,
    FOREIGN KEY (grade_level_id) REFERENCES grade_levels (id),
    FOREIGN KEY (academic_year_id) REFERENCES academic_years (id),
    UNIQUE (academic_year_id, grade_level_id, name)
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classroom_id INTEGER,
    student_code TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    birth_date TEXT,
    gender TEXT CHECK (gender IN ('male', 'female')),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'graduated', 'transferred')),
    notes TEXT,
    FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS guardians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS student_guardians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    guardian_id INTEGER NOT NULL,
    relationship TEXT,
    is_primary INTEGER NOT NULL DEFAULT 0,
    can_receive_messages INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (guardian_id) REFERENCES guardians (id) ON DELETE CASCADE,
    UNIQUE (student_id, guardian_id)
);

CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    employee_code TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    department TEXT,
    phone TEXT,
    hire_date TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL UNIQUE,
    specialization TEXT,
    max_periods_per_week INTEGER,
    FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    code TEXT UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS teacher_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
    UNIQUE (teacher_id, subject_id)
);

CREATE TABLE IF NOT EXISTS class_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classroom_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    weekly_periods INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
    UNIQUE (classroom_id, subject_id)
);

CREATE TABLE IF NOT EXISTS teacher_class_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    classroom_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    academic_year_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE,
    FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years (id) ON DELETE CASCADE,
    UNIQUE (teacher_id, classroom_id, subject_id, academic_year_id)
);

CREATE TABLE IF NOT EXISTS periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    starts_at TEXT NOT NULL,
    ends_at TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    UNIQUE (name, starts_at, ends_at)
);

CREATE TABLE IF NOT EXISTS timetable_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term_id INTEGER NOT NULL,
    classroom_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
    room TEXT,
    FOREIGN KEY (term_id) REFERENCES terms (id) ON DELETE CASCADE,
    FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES periods (id) ON DELETE CASCADE,
    UNIQUE (term_id, classroom_id, weekday, period_id),
    UNIQUE (term_id, teacher_id, weekday, period_id)
);

CREATE TABLE IF NOT EXISTS substitutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timetable_entry_id INTEGER NOT NULL,
    absent_teacher_id INTEGER NOT NULL,
    substitute_teacher_id INTEGER,
    substitute_staff_id INTEGER,
    substitution_date TEXT NOT NULL,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'planned' CHECK (status IN ('planned', 'completed', 'cancelled')),
    FOREIGN KEY (timetable_entry_id) REFERENCES timetable_entries (id) ON DELETE CASCADE,
    FOREIGN KEY (absent_teacher_id) REFERENCES teachers (id),
    FOREIGN KEY (substitute_teacher_id) REFERENCES teachers (id),
    FOREIGN KEY (substitute_staff_id) REFERENCES staff (id),
    UNIQUE (timetable_entry_id, substitution_date)
);

CREATE TABLE IF NOT EXISTS waiting_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    substitution_id INTEGER,
    classroom_id INTEGER NOT NULL,
    supervisor_staff_id INTEGER,
    period_id INTEGER NOT NULL,
    session_date TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (substitution_id) REFERENCES substitutions (id) ON DELETE SET NULL,
    FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE,
    FOREIGN KEY (supervisor_staff_id) REFERENCES staff (id) ON DELETE SET NULL,
    FOREIGN KEY (period_id) REFERENCES periods (id) ON DELETE CASCADE,
    UNIQUE (classroom_id, period_id, session_date)
);

CREATE TABLE IF NOT EXISTS staff_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    attendance_date TEXT NOT NULL,
    check_in_at TEXT,
    check_out_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('present', 'absent', 'late', 'excused')),
    notes TEXT,
    FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE,
    UNIQUE (staff_id, attendance_date)
);

CREATE TABLE IF NOT EXISTS student_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    classroom_id INTEGER NOT NULL,
    attendance_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('present', 'absent', 'late', 'excused')),
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE CASCADE,
    UNIQUE (student_id, attendance_date)
);

CREATE TABLE IF NOT EXISTS communications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guardian_id INTEGER,
    student_id INTEGER,
    created_by_user_id INTEGER,
    channel TEXT NOT NULL CHECK (channel IN ('phone', 'sms', 'whatsapp', 'email', 'meeting', 'note')),
    subject TEXT,
    body TEXT NOT NULL,
    communication_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    follow_up_at TEXT,
    FOREIGN KEY (guardian_id) REFERENCES guardians (id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE SET NULL,
    FOREIGN KEY (created_by_user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by_user_id INTEGER,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    audience TEXT NOT NULL CHECK (audience IN ('all', 'teachers', 'staff', 'guardians', 'students')),
    published_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by_user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by_user_id INTEGER,
    student_id INTEGER,
    teacher_id INTEGER,
    staff_id INTEGER,
    classroom_id INTEGER,
    title TEXT NOT NULL,
    report_type TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by_user_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE SET NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE SET NULL,
    FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE SET NULL,
    FOREIGN KEY (classroom_id) REFERENCES classrooms (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uploaded_by_user_id INTEGER,
    title TEXT NOT NULL,
    document_type TEXT NOT NULL,
    source_path TEXT,
    source_url TEXT,
    mime_type TEXT,
    visibility TEXT NOT NULL DEFAULT 'internal' CHECK (visibility IN ('public', 'internal', 'private')),
    content_hash TEXT UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by_user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER,
    embedding_id TEXT,
    page_number INTEGER,
    metadata_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE,
    UNIQUE (document_id, chunk_index)
);

CREATE TABLE IF NOT EXISTS document_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS document_tag_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES document_tags (id) ON DELETE CASCADE,
    UNIQUE (document_id, tag_id)
);

CREATE TABLE IF NOT EXISTS chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_session_id INTEGER NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_session_id) REFERENCES chat_sessions (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS retrieval_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_message_id INTEGER NOT NULL,
    document_chunk_id INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    score REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_message_id) REFERENCES chat_messages (id) ON DELETE CASCADE,
    FOREIGN KEY (document_chunk_id) REFERENCES document_chunks (id) ON DELETE CASCADE,
    UNIQUE (chat_message_id, document_chunk_id)
);

CREATE INDEX IF NOT EXISTS idx_students_classroom_id ON students (classroom_id);
CREATE INDEX IF NOT EXISTS idx_staff_job_title ON staff (job_title);
CREATE INDEX IF NOT EXISTS idx_timetable_lookup ON timetable_entries (term_id, weekday, period_id);
CREATE INDEX IF NOT EXISTS idx_staff_attendance_date ON staff_attendance (attendance_date);
CREATE INDEX IF NOT EXISTS idx_student_attendance_date ON student_attendance (attendance_date);
CREATE INDEX IF NOT EXISTS idx_documents_type ON documents (document_type);
CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id ON document_chunks (document_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages (chat_session_id);
