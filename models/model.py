from pydantic import  BaseModel

class HRCreate(BaseModel):
    name: str
    email: str
class HrCreateJob(BaseModel):
    hr_id:str
    job_title: str
    job_description: str
    freshers:bool | None = False
    experienced:bool | None = False
