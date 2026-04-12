# # grader.py

# def grade(question: str, student_answer: str, rubric: str) -> float:
#     """
#     Grades a student's answer based on a simple heuristic.

#     Args:
#         question (str): The question asked
#         student_answer (str): The student's response
#         rubric (str): Expected answer / guideline

#     Returns:
#         float: Score between 0.0 and 1.0
#     """

#     # Safety checks
#     if not student_answer or not rubric:
#         return 0.0

#     # Normalize text
#     student_answer = student_answer.lower().strip()
#     rubric = rubric.lower().strip()

#     # Tokenize
#     student_words = set(student_answer.split())
#     rubric_words = set(rubric.split())

#     if not rubric_words:
#         return 0.0

#     # Calculate overlap score
#     common_words = student_words.intersection(rubric_words)
#     score = len(common_words) / len(rubric_words)

#     # Clamp score between 0 and 1
#     score = max(0.0, min(1.0, score))

#     return score
# def grade(observation, action, info):
#     """
#     Calculates the reward based on the difference between expected and predicted scores.
#     Ensures the output is strictly within the (0.01, 0.99) range.
#     """
#     try:
#         # Ensure we are working with floats to avoid type errors
#         expected = float(info.get("expected_score", 0))
#         predicted = float(info.get("agent_score", 0))

#         # Calculate absolute difference
#         diff = abs(predicted - expected)

#         # Base score calculation (Normalized to 1.0)
#         # Assuming the max possible score in your dataset is 10.0
#         score = 1.0 - (diff / 10.0)

#         # 🔥 Clamp STRICTLY between 0.01 and 0.99
#         # This prevents the 'Out of Range' error from the validator
#         if score <= 0.0:
#             score = 0.01
#         elif score >= 1.0:
#             score = 0.99
#         else:
#             score = float(score)

#         return score

#     except Exception as e:
#         # Fallback reward so the validator doesn't crash if info is missing
#         print(f"Grader Error: {e}")
#         return 0.5

# Grader.py
from typing import Dict, Any

class Grader:
    def __init__(self, task_id: str):
        self.task_id = task_id

    def grade(self, observation: Dict[str, Any], action: Dict[str, Any]) -> float:
        """
        observation: contains 'rubric_score'
        action: contains 'score' (agent prediction)
        returns: reward between 0.0 and 1.0
        """
        try:
            true_score = float(observation.get("rubric_score", 0))
            pred_score = float(action.get("score", 0))

            # reward = 1 - normalized difference
            diff = abs(true_score - pred_score) / 10.0
            reward = max(0.0, 1.0 - diff)

            # 🔹 Log step for validator parsing
            print(
                f"[GRADER] task={self.task_id} true_score={true_score:.2f} "
                f"pred_score={pred_score:.2f} reward={reward:.3f}",
                flush=True
            )

            return reward
        except Exception as e:
            print(f"[GRADER] task={self.task_id} error={e}", flush=True)
            return 0.0
