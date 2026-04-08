
import asyncio
import os
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv()


from openai import OpenAI

# 🔹 Your environment
from server.environment import ExamEnv
from server.models import Action

# ==============================
# CONFIGURATION
# ==============================


# API_KEY = os.getenv("HF_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")
# API_BASE_URL = os.getenv("API_BASE_URL") or "https://api-inference.huggingface.co/models"
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
# IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

TASK_NAME = "exam-evaluator"
BENCHMARK = "exam_env"
MAX_STEPS = 5
SUCCESS_SCORE_THRESHOLD = 0.1
MAX_SCORE_PER_STEP = 10.0  # max marks per step

# ==============================
# SYSTEM PROMPT
# ==============================
SYSTEM_PROMPT = """
You are an AI exam evaluator.

You will be given:
- Question
- Student Answer
- Rubric (total marks = 10)

Your task:
- Assign a score between 1 and 10

Rules:
- Follow rubric strictly
- Be fair and consistent
- Return ONLY a number (no explanation)
"""

# ==============================
# LOGGING FUNCTIONS
# ==============================
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True
    )


def build_prompt(obs, step, history):
    return f"""
You are an exam evaluator improving your score step by step.

Step: {step}/5

Question:
{obs['question']}

Student Answer:
{obs['student_answer']}

Rubric:
{obs['rubric']}

Previous Attempts:
{history}

Instructions:
- Try to improve your score each step
- Learn from previous attempts
- Give ONLY a number between 0 to 10

Output format:
{{"score": <number>}}
"""

def get_score(client, obs, step, history):

    prompt = f"""
You are an exam evaluator improving your score step by step.

Step: {step}/5

Question:
{obs.question}

Student Answer:
{obs.student_answer}

Rubric:
{obs.rubric}

Previous Attempts:
{history}

Instructions:
- Try to improve your score each step
- Learn from previous attempts
- Give ONLY a number between 0 to 10

Output format:
{{"score": <number>}}
"""

    # 🔹 your existing model call
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=[{"role": "user", "content": prompt}],
    )

    # 🔹 extract score (keep your existing parsing)
    import re
    match = re.search(r"\d+", response.choices[0].message.content)
    return int(match.group()) if match else 0
# ==============================
# MAIN
# ==============================
def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    # Docker image or local env
    env = ExamEnv()  # Just create the environment normally

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

    try:
        # obs = env.reset()
        obs = env.reset()
        if isinstance(obs, tuple):
           obs = obs[0]

        
        
        history = []  # 🔥 NEW

        for step in range(1, MAX_STEPS + 1):

    # 🔥 UPDATED: pass step + history
          score_pred = get_score(client, obs, step, history)

          action = Action(score=score_pred)

          obs, reward, done, info = env.step(action)

    # 🔹 handle reward object
          if hasattr(reward, "value"):
            reward = reward.value
          elif hasattr(reward, "score"):
            reward = reward.score
          else:
            reward = float(reward) if reward is not None else 0.0

          error = None

          rewards.append(reward)
          steps_taken = step

    # 🔥 ADD history
          history.append(f"Step {step}: score={score_pred}, reward={reward}")

          log_step(step, str(int(score_pred)), reward, done, error)

          if done:
            break

        # max_total = MAX_STEPS * MAX_SCORE_PER_STEP
        # score = sum(rewards) / max_total if max_total > 0 else 0.0
        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    finally:
        try:
            pass
        except Exception as e:
            print(f"[DEBUG] close error: {e}", flush=True)
        log_end(success, steps_taken, score, rewards)

if __name__ == "__main__":
    main()