# server/main.py
from fastapi import FastAPI
from server import models  # import your Pydantic models

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI in Docker!"}

# Example endpoint using your Observation model
@app.post("/evaluate")
def evaluate(observation: models.Observation):
    # Just a placeholder response for now
    return {
        "question": observation.question,
        "student_answer": observation.student_answer,
        "rubric": observation.rubric,
        "score": 0.0,
        "feedback": "Evaluation logic not yet implemented"
    }
