from fastapi import FastAPI
from pydantic import BaseModel
from api_pipeline import run_pipeline
from fastapi.middleware.cors import CORSMiddleware
print("🟢 main.py loaded")
app = FastAPI()

class URLInput(BaseModel):
    url: str  

origins = [
    "https://genre-prediction-8knm.onrender.com",  # React dev server
    # "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # allow React frontend
    allow_credentials=True,
    allow_methods=["*"],            # allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],            # allow all headers
)
@app.get("/")
def read_root():
    return {"status": "FastAPI is running on Render!"}
@app.get("/recommend")
def read_root():
    return {"status": "recommend is running on Render!"}
@app.post("/recommend")
def recommend_from_url(input: URLInput):
    print("⭕️ recommend_from_url")
    result = run_pipeline(input.url)  
    return {"result": result}
