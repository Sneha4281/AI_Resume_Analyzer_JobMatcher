import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_db():
    conn = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")

    )
    return conn


def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # USERS (Candidates)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id  VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # HR USERS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hr_users (
            hr_id VARCHAR(100) PRIMARY KEY ,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            role VARCHAR(50) DEFAULT 'HR',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # JOBS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id VARCHAR(100) PRIMARY KEY,
            job_title VARCHAR(150) NOT NULL,
            job_description TEXT NOT NULL,
            freshers BOOLEAN DEFAULT FALSE,
            experienced BOOLEAN DEFAULT FALSE,
            created_by VARCHAR(150) REFERENCES hr_users(hr_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # RESUMES
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            resume_id VARCHAR(100) PRIMARY KEY,
            user_id VARCHAR(150)  REFERENCES users(user_id),
            job_id VARCHAR(150)  REFERENCES jobs(job_id),
            resume_text TEXT,
            resume_file VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # MATCH RESULTS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS match_results (
            match_id VARCHAR(100) PRIMARY KEY,
            resume_id VARCHAR(100) REFERENCES resumes(resume_id),
            job_id VARCHAR(100) REFERENCES jobs(job_id),
            matching_score INTEGER,
            matching_skills TEXT[],
            missing_skills TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # EMAIL LOGS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS email_logs (
            email_id VARCHAR(100) PRIMARY KEY,
            resume_id VARCHAR(100) REFERENCES resumes(resume_id),
            job_id VARCHAR(100) REFERENCES jobs(job_id),
            email_type VARCHAR(50),
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All tables created successfully")


if __name__ == "__main__":
    create_tables()



 # uvicorn main:app --reload --port 8000