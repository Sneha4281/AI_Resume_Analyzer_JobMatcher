import uvicorn
from fastapi import FastAPI
app = FastAPI()
from service import path_function

@app.get("/")
def root():
    return {"message":"Hello World"}

app.include_router(path_function.router,tags=["AI RESUME ANALYZER AND JOB MATCHER"])

if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost",port=59904)
