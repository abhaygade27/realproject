# from fastapi import FastAPI
# from environment import ExamEnv
# from models import Observation, Action, Reward

# app = FastAPI()
# env = ExamEnv()

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI in hi Docker!"}

# @app.get("/health")
# def health_check():
#     return {"status": "ok"}


# @app.post("/reset")
# def reset(difficulty: str = None):
#     obs = env.reset(difficulty)
#     return obs.dict()

# @app.post("/step")
# def step(action: Action):
#     obs, reward, done, info = env.step(action)
#     return {
#         "observation": obs,
#         "reward": reward.value,
#         "done": done,
#         "info": info
#     }

# @app.get("/state")
# def state():
#     return env.state()

from fastapi import FastAPI
from server.environment import ExamEnv

# from envs.realproject.environment import ExamEnv


import os
port = int(os.environ.get("PORT", 7860))

from server.models import Observation, Action, Reward

app = FastAPI()

# 🔹 Initialize env globally for initial use (optional)
env = ExamEnv()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI in hi Docker!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# 🔹 Reset endpoint now reloads environment every time
@app.post("/reset")
def reset(difficulty: str = None):
    global env
    env = ExamEnv()  # Re-initialize to pick up updated dataset
    obs = env.reset(difficulty)
    return obs.dict()

@app.post("/step")
def step(action: Action):
    # Ensure using current env
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.value,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    # Always return current state
    return env.state()