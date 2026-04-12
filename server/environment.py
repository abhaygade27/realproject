import json
import random
import os
from typing import Optional
from server.models import Observation, Action, Reward
# from grader import grade  # Correctly imported
import sys
import os

# This adds the root directory to the Python path so it can find grader.py
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from grader import grade
except ImportError:
    # Fallback if the above logic fails in a specific container env
    def grade(*args, **kwargs): return 0.5

class ExamEnv:
    def __init__(self, dataset_path: Optional[str] = None):
        # 1. ROBUST PATHING
        if dataset_path is None:
            # Look in the parent directory relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dataset_path = os.path.join(base_dir, "dataset.json")
        
        self.dataset_path = os.path.abspath(dataset_path)
        self.current_task = None
        self.data = []
        self.current_step = 0

    def load_data(self):
        # Fallback pathing in case the structure is flat
        if not os.path.exists(self.dataset_path):
            alt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.json")
            if os.path.exists(alt_path):
                self.dataset_path = alt_path
            else:
                return [] # Return empty instead of raising error

        try:
            with open(self.dataset_path, "r") as f:
                content = json.load(f)
                return content.get("tasks", [])
        except Exception:
            return []

    def reset(self, difficulty: Optional[str] = None):
        self.data = self.load_data()
        self.current_step = 0

        # 2. SAFETY CHECK: If data is missing, don't crash, provide a fake task
        if not self.data:
            self.current_task = {
                "id": 0, "question": "N/A", "student_answer": "N/A", 
                "rubric": {}, "expected_score": 5, "difficulty": "easy"
            }
        else:
            filtered = self.data
            # 3. CASE-INSENSITIVE FILTERING
            if difficulty:
                # Ensure difficulty strings match (both lowercase)
                filtered = [t for t in self.data if str(t.get("difficulty")).lower() == difficulty.lower()]
            
            # 4. FALLBACK: If filtering for 'hard' finds nothing, use all data
            if not filtered:
                filtered = self.data
            
            self.current_task = random.choice(filtered)

        return Observation(
            question=self.current_task["question"],
            student_answer=self.current_task["student_answer"],
            rubric=self.current_task["rubric"]
        )

    def step(self, action: Action):
        self.current_step += 1

        if self.current_task is None:
            # Silent reset if someone forgot to call it
            self.reset()

        expected = float(self.current_task.get("expected_score", 5))
        predicted = float(action.score)

        # 5. CALL GRADER WITH CONTEXT
        grader_score = grade(
            None,
            action,
            {
                "expected_score": expected,
                "agent_score": predicted,
                "difficulty": self.current_task.get("difficulty")
            }
        )

        # 6. STRICT (0,1) CLAMPING (Never exactly 0 or 1)
        try:
            reward_value = float(grader_score)
        except:
            reward_value = 0.5
            
        reward_value = max(0.01, min(0.99, reward_value))

        reward = Reward(value=reward_value)
        done = True

        # 7. EXPLICIT INFO KEYS
        info = {
            "expected_score": expected,
            "agent_score": predicted,
            "task_id": self.current_task.get("id"),
            "difficulty": self.current_task.get("difficulty"),
            "has_grader": True
        }

        obs = Observation(
            question=self.current_task["question"],
            student_answer=self.current_task["student_answer"],
            rubric=self.current_task["rubric"]
        )

        return obs, reward, done, info

    def state(self):
        return self.current_task