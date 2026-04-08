# import json
# import random
# import os
# from typing import Optional
# from models import Observation, Action, Reward



# class ExamEnv:
#     def __init__(self, dataset_path: str = "dataset.json"):                                                                                                                                       
#         base_dir = os.path.dirname(__file__)
#         self.dataset_path = os.path.join(base_dir, dataset_path)

#         with open(self.dataset_path, "r") as f:
#             self.data = json.load(f)["tasks"]

#         self.current_task = None

#     def reset(self, difficulty: Optional[str] = None):
#         if difficulty:
#             filtered = [t for t in self.data if t["difficulty"] == difficulty]
#             if not filtered:
#                 raise ValueError("No tasks found")
#             self.current_task = random.choice(filtered)
#         else:
#             self.current_task = random.choice(self.data)

#         return Observation(
#             question=self.current_task["question"],
#             student_answer=self.current_task["student_answer"],
#             rubric=self.current_task["rubric"]
#         )

#     def step(self, action: Action):
#         expected = self.current_task["expected_score"]
#         diff = abs(action.score - expected)

#         if diff == 0:
#             reward_value = 1.0
#             feedback = "Perfect grading"
#         elif diff <= 1:
#             reward_value = 0.8
#             feedback = "Very close"
#         elif diff <= 2:
#             reward_value = 0.5
#             feedback = "Partially correct"
#         else:
#             reward_value = 0.0
#             feedback = "Incorrect grading"

#         reward = Reward(
#             value=reward_value,
#             feedback=feedback
#         )

#         done = True

#         info = {
#             "expected_score": expected,
#             "agent_score": action.score
#         }

#         # Return a new observation (same question)
#         obs = Observation(
#             question=self.current_task["question"],
#             student_answer=self.current_task["student_answer"],
#             rubric=self.current_task["rubric"]
#         )

#         return obs, reward, done, info

#     def state(self):
#         return self.current_task


import json
import random
import os
from typing import Optional
from .models import Observation, Action, Reward



class ExamEnv:
    def __init__(self, dataset_path: str = "dataset.json"):
        base_dir = os.path.dirname(__file__)
        self.dataset_path = os.path.join(base_dir, dataset_path)
        self.current_task = None

    # 🔹 Load dataset dynamically
    def load_data(self):
        with open(self.dataset_path, "r") as f:
            return json.load(f)["tasks"]

    def reset(self, difficulty: Optional[str] = None):
        # 🔹 Always load the latest dataset here
        self.data = self.load_data()

        if difficulty:
            filtered = [t for t in self.data if t["difficulty"] == difficulty]
            if not filtered:
                raise ValueError("No tasks found")
            self.current_task = random.choice(filtered)
        else:
            self.current_task = random.choice(self.data)

        return Observation(
            question=self.current_task["question"],
            student_answer=self.current_task["student_answer"],
            rubric=self.current_task["rubric"]
        )

    def step(self, action: Action):
        expected = self.current_task["expected_score"]
        diff = abs(action.score - expected)

        print(f"Expected: {expected}, Predicted: {action.score}, Diff: {diff}")
 
        # if diff == 0:
        #     reward_value = 1.0
            
        # elif diff <= 1:
        #     reward_value = 0.8
            
        # elif diff <= 2:
        #     reward_value = 0.5
            
        # else:
        #     reward_value = 0.0
        reward_value = max(0, 1 - (diff / 10))
            

        reward = Reward(
            value=reward_value

        )

        done = True

        info = {
            "expected_score": expected,
            "agent_score": action.score
        }

        # Return a new observation (same question)
        obs = Observation(
            question=self.current_task["question"],
            student_answer=self.current_task["student_answer"],
            rubric=self.current_task["rubric"]
        )

        return obs, reward, done, info

    def state(self):
        return self.current_task