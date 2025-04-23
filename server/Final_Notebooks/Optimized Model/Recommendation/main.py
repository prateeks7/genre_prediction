from fastapi import FastAPI
from pydantic import BaseModel
from api_pipeline import run_pipeline


app = FastAPI()

class URLInput(BaseModel):
    url: str  

@app.post("/recommend")
def recommend_from_url(input: URLInput):
    result = run_pipeline(input.url)  
    return {"result": result}
