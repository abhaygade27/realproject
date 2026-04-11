# import json
# from server.environment import ExamEnv
# from server.models import Action

# def load_dataset(path="dataset.json"):
#     """Load dataset.json and return list of tasks."""
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)["tasks"]

# def grade_all_tasks():
#     env = ExamEnv(dataset_path="dataset.json")
#     tasks = load_dataset()

#     results = {}

#     for difficulty in ["easy", "medium", "hard"]:
#         filtered = [t for t in tasks if t["difficulty"] == difficulty]
#         if not filtered:
#             continue

#         print(f"\n--- Evaluating {difficulty.upper()} tasks ---")
#         diffs = []

#         for task in filtered:
#             # Reset environment with this difficulty
#             obs = env.reset(difficulty=difficulty)

#             # Create an Action using expected_score as proxy (baseline agent)
#             action = Action(score=task["expected_score"])

#             # Step through environment
#             obs, reward, done, info = env.step(action)

#             diff = abs(info["agent_score"] - info["expected_score"])
#             diffs.append(diff)

#             print(f"Q: {obs.question}")
#             print(f"Expected: {info['expected_score']}, Agent: {info['agent_score']}, Reward: {reward.value:.3f}\n")

#         avg_diff = sum(diffs) / len(diffs) if diffs else 0.0
#         results[difficulty] = avg_diff

#     return results

# if __name__ == "__main__":
#     summary = grade_all_tasks()
#     print("\n=== Final Grading Summary ===")
#     for diff, avg in summary.items():
#         print(f"{diff.capitalize()}: Avg difference = {avg:.3f}")
def grade(observation, action, info):
    expected = info["expected_score"]
    predicted = info["agent_score"]

    diff = abs(predicted - expected)

    # normalize to [0,1]
    score = max(0.0, 1.0 - (diff / 10.0))

    return scoregit 