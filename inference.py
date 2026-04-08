import asyncio
import os
from typing import List, Optional

from openai import OpenAI

# 🔹 Import your environment
from server.environment import ExamEnv
from server.models import Action

# ==============================
# CONFIGURATION
# ==============================
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")  # 🔥 required for docker

TASK_NAME = "exam-evaluator"
BENCHMARK = "exam_env"

MAX_STEPS = 5
SUCCESS_SCORE_THRESHOLD = 0.1
MAX_SCORE_PER_STEP = 10.0  # since your scoring is 1–10

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
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={str(done).lower()} error={error_val}",
        flush=True
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.3f} rewards={rewards_str}",
        flush=True
    )

# ==============================
# BUILD PROMPT
# ==============================
def build_prompt(obs) -> str:
    return f"""
Question:
{obs.question}

Student Answer:
{obs.student_answer}

Rubric:
{obs.rubric}

Give score (1–10):
"""

# ==============================
# MODEL CALL
# ==============================
def get_score(client: OpenAI, obs) -> float:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_prompt(obs)},
            ],
            temperature=0.2,
            max_tokens=10,
        )

        text = (response.choices[0].message.content or "").strip()
        score = float(text)

        return max(1.0, min(10.0, score))

    except Exception as e:
        print(f"[DEBUG] Model error: {e}", flush=True)
        return 5.0

# ==============================
# MAIN
# ==============================
async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    # 🔥 Correct OpenEnv usage
    env = await ExamEnv.from_docker_image(IMAGE_NAME)

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

    try:
        # 🔹 Start episode
        result = await env.reset()
        obs = result.observation

        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            # 🔹 Get model score
            score_pred = get_score(client, obs)

            # 🔹 Convert to string for logging
            action_str = str(int(score_pred))

            # 🔹 Step environment
            result = await env.step(Action(score=score_pred))
            obs = result.observation

            reward = result.reward or 0.0
            done = result.done
            error = None

            rewards.append(reward)
            steps_taken = step

            # 🔹 Log step
            log_step(step, action_str, reward, done, error)

            if done:
                break

        # 🔹 Normalize score to [0,1]
        max_total = MAX_STEPS * MAX_SCORE_PER_STEP
        score = sum(rewards) / max_total if max_total > 0 else 0.0
        score = min(max(score, 0.0), 1.0)

        success = score >= SUCCESS_SCORE_THRESHOLD

    finally:
        try:
            await env.close()
        except Exception as e:
            print(f"[DEBUG] close error: {e}", flush=True)

        log_end(success, steps_taken, score, rewards)

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    asyncio.run(main())