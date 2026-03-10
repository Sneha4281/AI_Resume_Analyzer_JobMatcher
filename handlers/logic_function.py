from database.db import get_db
from utility.gen_uuid import generate_uuid
from utility.nlp_resume import extract_text_from_pdf,clean_text
from utility.email_service import send_email_notification
from utility.nlp_jd import extract_skills_from_job_description,calculate_matching_score
from utility.matching_data import find_matching_and_missing_skills
from fastapi import UploadFile,HTTPException
class Analyser:
    def Logic_create_hr(self,data):
        try:
            hr_id = generate_uuid()
            conn=get_db()
            curr=conn.cursor()
            curr.execute("""
            insert into hr_users (hr_id,name,email) values(%s,%s,%s)
            """,(hr_id,data.name,data.email))
            conn.commit()
            conn.close()
            return {
                "message":"success hr_name is added",
            }
        except Exception as e:
            return {
                "message":"error occured",
                "error":f"{str(e)}"
            }

    def Logic_hr_create_job(self,data):
        try:
            job_id = generate_uuid()
            conn=get_db()
            curr=conn.cursor()
            curr.execute("""
                         insert into jobs (job_id,job_title,job_description,freshers,experienced,created_by) values(%s,%s,%s,%s,%s,%s)""",(job_id,data.job_title,data.job_description,data.freshers,data.experienced,data.hr_id))
            conn.commit()
            conn.close()
            return {
                "message":"success job_name is added",
                "job_id":job_id,
            }
        except Exception as e:
            return {
                "message":"error occured",
                "error":f"{str(e)}"
            }
    def Logic_user_upload_resume(self,name: str,
        email: str,
        job_id: str,
        upload_resume: UploadFile):
        try:
            if not upload_resume.filename.endswith(".pdf"):
                raise HTTPException(status_code=404,detail="pdf resume file only")
            user_id=generate_uuid()
            conn=get_db()
            curr=conn.cursor()
            curr.execute("""
                         insert into users(user_id,name,email) values(%s,%s,%s)""",(user_id,name,email))
            raw_text = extract_text_from_pdf(upload_resume.file)
            resume_text=clean_text(raw_text)
            resume_id=generate_uuid()
            curr.execute("""
            insert into resumes(resume_id,user_id,job_id,resume_text,resume_file) values(%s,%s,%s,%s,%s)""",(resume_id,user_id,job_id,resume_text,upload_resume.filename))
            conn.commit()
            conn.close()
            return {
                "message":"success resume_id is added",
                "resume_id":resume_id,
            }
        except Exception as e:
            return {
                "message":"error occured",
                "error":f"{str(e)}"

            }
    def Logic_get_job_info(self):
        try:
            conn=get_db()
            curr=conn.cursor()
            curr.execute("""
            select job_id,job_title,job_description,freshers,experienced from jobs""")
            rows=curr.fetchall()
            conn.close()
            conn.close()
            jobs=[]
            for row in rows:
                jobs.append({
                    "job_id":row[0],
                    "job_title":row[1],
                    "job_description":row[2],
                    "freshers":row[3],
                    "experienced":row[4],
                })
            return {
            "message":"success ",
            "jobs":jobs
            }
        except Exception as e:
            return {
                "message":"error occured",
                "error":f"{str(e)}"
            }

    def Logic_run_matching(self):
        try:
            conn=get_db()
            curr=conn.cursor()
            curr.execute("""
            select r.resume_id,
            r.resume_text,
            r.user_id,
            r.job_id,
            j.job_description,
            u.email
            from resumes r
            join jobs j on r.job_id=j.job_id
            join users u on r.user_id=u.user_id""")
            records=curr.fetchall()
            results=[]
            for row in records:
                resume_id=row[0]
                resume_text=row[1]
                user_id=row[2]
                job_id=row[3]
                job_description=row[4]
                email=row[5]

                job_skills=extract_skills_from_job_description(job_description)

                matching_score=calculate_matching_score(
                    resume_text,
                    job_description
                )

                matching_skills,missing_skills=find_matching_and_missing_skills(
                job_skills,
                resume_text
                )
                if matching_score>60:
                    status="POSITIVE"
                    message=(
                        "Congratulations!\n\n"
                        "Your profile matches our job requirements.\n"
                        "Our HR team will contact you for the next steps."
                    )

                else:
                    status="NEGATIVE"
                    message=(
                        "Thank you for applying.\n\n"
                        "Your profile does not match our current requirements.\n"
                        f"Missing skills: {missing_skills}"
                    )

                send_email_notification(email, message)


                results.append({
                    "resume_id":resume_id,
                    "job_id":job_id,
                    "matching_score":matching_score,
                    "missing_skills":missing_skills,
                    "status":status
                })

            curr.close()
            conn.close()
            return{
                    "message":"matching completed",
                    "data":results
                }
        except Exception as e:
            return {
                "message":"error occured",
                "error":f"{str(e)}"
            }

