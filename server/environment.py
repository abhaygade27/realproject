

import json
import random
import os
from typing import Optional
from server.models import Observation, Action, Reward
from grader import grade   # 🔥 IMPORTANT


class ExamEnv:
    def __init__(self, dataset_path: Optional[str] = None):
        self.prev_diff = None

        if dataset_path is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            dataset_path = os.path.join(base_dir, "dataset.json")

        self.dataset_path = os.path.abspath(dataset_path)
        self.current_task = None
        self.data = []
        self.current_step = 0

    def load_data(self):
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")

        with open(self.dataset_path, "r") as f:
            return json.load(f)["tasks"]

    def reset(self, difficulty: Optional[str] = None):
        self.prev_diff = None
        self.data = self.load_data()
        self.current_step = 0

        if not self.data:
            raise ValueError("Dataset is empty")

        filtered = self.data

        if difficulty:
            filtered = [t for t in self.data if t.get("difficulty") == difficulty]

            if not filtered:
                raise ValueError(f"No tasks found for difficulty: {difficulty}")

        self.current_task = random.choice(filtered)

        return Observation(
            question=self.current_task["question"],
            student_answer=self.current_task["student_answer"],
            rubric=self.current_task["rubric"]
        )

    def step(self, action: Action):
        self.current_step += 1

        if self.current_task is None:
            raise RuntimeError("Environment not reset. Call reset() first.")

        expected = self.current_task["expected_score"]
        predicted = action.score

        diff = abs(predicted - expected)

        # 🔥 CALL GRADER (THIS FIXES MAIN ERROR)
        grader_score = grade(
            None,
            action,
            {
                "expected_score": expected,
                "agent_score": predicted
            }
        )

        # 🔥 ensure strict (0,1)
        reward_value = max(0.01, min(0.99, grader_score))

        reward = Reward(value=reward_value)

        # since MAX_STEPS = 1
        done = True

        info = {
            "expected_score": expected,
            "agent_score": predicted,
            "diff": diff,
            "task_id": self.current_task.get("task_id", "unknown")
        }

        obs = Observation(
            question=self.current_task["question"],
            student_answer=self.current_task["student_answer"],
            rubric=self.current_task["rubric"]
        )

        return obs, reward, done, info

    def state(self):
        return self.current_task