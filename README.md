---
title: Real Project Environment
emoji: "🤖"
colorFrom: "blue"
colorTo: "green"
sdk: "docker"
app_file: Dockerfile
pinned: true
---

---

title: Real Project Environment
colorFrom: "blue"
colorTo: "green"
sdk: "docker"
app_file: Dockerfile
pinned: true
------------

# AI Exam Evaluator (OpenEnv Environment)

An AI-based automated grading environment where agents evaluate student answers using structured rubrics.

This project simulates a real-world educational task used in universities and ed-tech platforms: grading subjective answers with partial credit.

---

# Motivation

Manual grading is:

* Time-consuming
* Inconsistent
* Difficult to scale

This environment enables AI agents to:

* Understand student answers
* Align with grading rubrics
* Provide structured feedback and scoring

---

# Environment Overview

The environment follows the OpenEnv specification:

* reset() → starts a new grading task
* step(action) → agent submits evaluation
* state() → returns current state

---

# Observation Space

The agent receives:

```json
{
  "question": "Exam question",
  "student_answer": "Student response text",
  "rubric": {
    "keywords": ["force", "mass", "acceleration"],
    "concept": "F = ma",
    "marks": 10
  }
}
```

---

# Action Space

The agent must return:

```json
{
  "score": 0.0,
  "feedback": "Detailed explanation of grading"
}
```

---

# Reward Function

The environment uses a deterministic multi-factor grading system:

* Keyword match → 40%
* Concept understanding → 20%
* Completeness → 20%
* Clarity and structure → 20%

Example logic:

```python
score = keyword_score + concept_score + completeness + clarity
score = min(score, 1.0)
```

Penalties:

* Very short answer → −0.2
* Irrelevant answer → −0.3

---

# Tasks

Easy:

* Simple factual questions
* Focus on keyword matching

Medium:

* Requires explanation and reasoning
* Focus on concept and structure

Hard:

* Analytical and applied problems
* Requires concept understanding, example or calculation, and complete explanation

---

# Example Task

```json
{
  "question": "Explain Newton’s Second Law",
  "student_answer": "Force equals mass times acceleration...",
  "rubric": {
    "keywords": ["force", "mass", "acceleration"],
    "concept": "F = ma"
  }
}
```

---

# API Endpoints

POST /reset
POST /step
GET /state

---

# Setup Instructions

Run with Docker:

```bash
docker build -t exam-env .
docker run -p 7860:7860 exam-env
```

Run without Docker:

```bash
pip install -r requirements.txt
uvicorn server.app:app --reload
```

---

# Baseline Inference

Run baseline agent:

```bash
export OPENAI_API_KEY=your_key
python server/inference.py
```

Example output:

```
Average Score: 0.62
```

---

# Project Structure

```
/app
 ├── server/
 │    ├── app.py
 │    ├── environment.py
 │    ├── models.py
 │    ├── grader.py
 │    ├── inference.py
 │    ├── dataset.json
 │    ├── __init__.py
 ├── openenv.yaml
 ├── Dockerfile
 ├── requirements.txt
 ├── README.md
```

---

# OpenEnv Compliance

* Typed Pydantic models
* step / reset / state implemented
* Deterministic reward function
* Multi-task support (easy to hard)
* openenv.yaml included

---

# Evaluation Design

* Continuous reward from 0.0 to 1.0
* Partial progress scoring
* Deterministic grading
* Difficulty progression
* Transparent scoring via info

---

# Deployment

This project is deployed on Hugging Face Spaces using Docker.

---

# Author

Abhay Gade

---

# License

MIT License
