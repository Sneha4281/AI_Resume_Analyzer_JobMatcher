

from models.model import HRCreate,HrCreateJob
from handlers.logic_function import Analyser
from fastapi import APIRouter, Form,UploadFile,File

router=APIRouter()
Ai=Analyser()

@router.post('/create_hr')
def create_hr(data: HRCreate):
    try:
        return Ai.Logic_create_hr(data)
    except Exception as e:
        return{
            "message":f"{str(e)}",
        }
@router.post('/hr_create_job')
def hr_create_job(data:HrCreateJob):
    try:
        return Ai.Logic_hr_create_job(data)
    except Exception as e:
        return{
            "message":f"{str(e)}",
        }

@router.post('/user_upload_resume')
def user_upload_resume(
        name:str=Form(...),
        email:str=Form(...),
        job_id:str=Form(...),
        upload_resume:UploadFile=File(...)
):
    try:
        return  Ai.Logic_user_upload_resume(
            name=name,
            email=email,
            job_id=job_id,
            upload_resume=upload_resume
        )
    except Exception as e:
        return{
            "message":f"{str(e)}",
        }

@router.get('/get_job_info')
def get_resume_info():
    try:
        return Ai.Logic_get_job_info()
    except Exception as e:
        return {
            "message":f"{str(e)}",
        }

@router.get('/run_matching')
def run_matching():
    try:
        return Ai.Logic_run_matching()
    except Exception as e:
        return {
            "message":f"{str(e)}",
        }
