import logging
import sqlite3

logger = logging.getLogger(__name__)

def initialize_schema(conn):
    """Initializes database schema."""
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     goal TEXT,
                     study_schedule TEXT
                     )''')
        c.execute('''CREATE TABLE IF NOT EXISTS exam_results (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     student_id INTEGER,
                     exam_date TEXT,
                     exam_type TEXT,
                     matematik INTEGER,
                     fizik INTEGER,
                     kimya INTEGER,
                     biyoloji INTEGER,
                     turkce INTEGER,
                     sosyal INTEGER,
                     geometri INTEGER,
                     matematik_wrong_topics TEXT,
                     fizik_wrong_topics TEXT,
                     kimya_wrong_topics TEXT,
                     biyoloji_wrong_topics TEXT,
                     turkce_wrong_topics TEXT,
                     sosyal_wrong_topics TEXT,
                     geometri_wrong_topics TEXT,
                     FOREIGN KEY(student_id) REFERENCES students(id)
                     )''')
        c.execute('''CREATE TABLE IF NOT EXISTS assignments (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     student_id INTEGER,
                     subject TEXT,
                     topic TEXT,
                     task TEXT,
                     youtube_link TEXT,
                     due_date TEXT,
                     status TEXT,
                     FOREIGN KEY(student_id) REFERENCES students(id)
                     )''')
        conn.commit()
        logger.info("Database schema initialized")
    except sqlite3.Error as e:
        logger.error(f"Schema initialization error: {e}")
        raise