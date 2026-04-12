
# from fastapi import FastAPI
# from server.environment import ExamEnv

# # from envs.realproject.environment import ExamEnv
# import os
# import uvicorn



# from server.models import Observation, Action, Reward

# app = FastAPI()

# # 🔹 Initialize env globally for initial use (optional)
# env = ExamEnv()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI in hi Docker!"}

# @app.get("/health")
# def health_check():
#     return {"status": "ok"}

# # 🔹 Reset endpoint now reloads environment every time
# @app.post("/reset")
# def reset(difficulty: str = None):
#     # global env
#     # env = ExamEnv()  # Re-initialize to pick up updated dataset
#     obs = env.reset(difficulty)
#     return obs.dict()

# @app.post("/step")
# def step(action: Action):
#     # Ensure using current env
#     obs, reward, done, info = env.step(action)
#     return {
#         "observation": obs.dict(),
#         "reward": reward.value,
#         "done": done,
#         "info": info
#     }

# @app.get("/state")
# def state():
#     # Always return current state
#     return env.state()
    
    
# def main():
#     port = int(os.environ.get("PORT", 7860))
#     uvicorn.run(app, host="0.0.0.0", port=port)

# if __name__ == "__main__":
#     main()
from fastapi import FastAPI
from server.environment import ExamEnv
from server.models import Observation, Action, Reward
import os
import uvicorn

app = FastAPI()

# ✅ Global env
env = ExamEnv()


@app.get("/")
def read_root():
    return {"message": "FastAPI is running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ✅ RESET (FIXED)
@app.post("/reset")
def reset(difficulty: str = None):
    global env  # ✅ IMPORTANT

    # ✅ Reinitialize environment every reset
    env = ExamEnv()

    obs = env.reset(difficulty)

    # ✅ Logging for validator
    print(f"[RESET] difficulty={difficulty}", flush=True)

    return obs.dict()


# ✅ STEP (IMPROVED)
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)

    # ✅ Logging for validator
    print(
        f"[STEP] action={action.dict()} reward={reward.value} done={done}",
        flush=True
    )

    return {
        "observation": obs.dict(),
        "reward": reward.value,
        "done": done,
        "info": info
    }


# ✅ STATE (SAFE)
@app.get("/state")
def state():
    try:
        current_state = env.state()

        print("[STATE] fetched", flush=True)

        return current_state
    except Exception as e:
        print(f"[STATE ERROR] {e}", flush=True)
        return {"error": str(e)}


# ✅ MAIN
def main():
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()