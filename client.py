import requests
import json
import os
from dotenv import load_dotenv
import re

load_dotenv()

BASE_URL = "http://localhost:8000"




def build_prompt(obs):
    return f"""
You are an exam evaluator.

Evaluate the student's answer based on the rubric and give a score.

Question: {obs['question']}

Student Answer: {obs['student_answer']}

Rubric: {obs['rubric']}

Give a score between 0 to 10.

Return ONLY JSON format:
{{"score": number}}

Do not explain anything.
"""

# def build_prompt(obs):
#     return f"""
# You are an exam evaluator.

# Question: {obs['question']}
# Student Answer: {obs['student_answer']}
# Rubric: {obs['rubric']}

# Return ONLY JSON. No explanation.

# Example:
# {{"score": 7}}
# """

# 🔹 Call Hugging Face API
# def call_model(prompt):
#     HF_API_URL = "https://router.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
#     headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}

#     # headers = {
#     #     "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
#     #     "Content-Type": "application/json"
#     # }
    

#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 50,
#             "temperature": 0.2,
#             "return_full_text": False
#         }
#     }

#     response = requests.post(HF_API_URL, headers=headers, json=payload)

#     if response.status_code != 200:
#         print("❌ HF Error:", response.status_code)
#         print("Raw:", response.text)
#         return '{"score": 0}'

#     try:
#         data = response.json()
#         return data[0]["generated_text"]
#     except:
#         print("❌ Parsing Error")
#         print(response.text)
#         return '{"score": 0}'

def call_model(prompt):
    HF_API_URL = "https://router.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"


    headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.2,
            "return_full_text": False
        }
    }

    resp = requests.post(HF_API_URL, headers=headers, json=payload)

    if resp.status_code == 200 and resp.text.strip():
        try:
            data = resp.json()
            return data[0]["generated_text"]
        except Exception as e:
            print("❌ Parsing Error:", e)
            print("Raw:", resp.text)
            return '{"score": 0}'
    else:
        print("❌ HF Error:", resp.status_code, resp.text)
        return '{"score": 0}'

    
def parse_response(text):
    import re

    print("⚠️ RAW OUTPUT:", text)

    # try JSON first
    try:
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return int(data.get("score", 0))
    except:
        pass

    # fallback: extract number
    numbers = re.findall(r"\d+", text)
    if numbers:
        return max(0, min(int(numbers[0]), 10))

    return 0   

# 🔹 Parse JSON response
# def parse_response(text):
#     try:
#         text = text.strip()
#         start = text.find("{")
#         end = text.rfind("}") + 1
#         json_str = text[start:end]
#         data = json.loads(json_str)
#         score = int(data["score"])
        
#         return score
#     except Exception as e:
#         print("❌ Parsing Error:", e)
#         print("⚠️ Raw Output:", text)
#         return 0

# 🔹 Agent
def agent(obs):
    prompt = build_prompt(obs)
    response = call_model(prompt)
    print("\nMODEL RAW OUTPUT:", response)
    return parse_response(response)

# 🔹 Run full pipeline
def run():
    for difficulty in ["easy", "medium", "hard"]:
        obs = requests.post(f"{BASE_URL}/reset", params={"difficulty": difficulty}).json()
        score = agent(obs)

        action = {
            "score": score
            
        }

        # result = requests.post(f"{BASE_URL}/step", json=action).json()
        resp = requests.post(f"{BASE_URL}/step", json=action)
        if resp.status_code == 200 and resp.text.strip():
           result = resp.json()
        else:
            print("❌ Server Error:", resp.status_code, resp.text)
            return



        print(f"\n--- {difficulty.upper()} ---")
        print(f"Agent Score: {score}")
        print(f"Reward: {result['reward']}")
        print(f"True Score: {result['info'].get('true_score')}")  
if __name__ == "__main__":
    run()

