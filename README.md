---
title: Real Project Environment
emoji: "🤖"
colorFrom: "blue"
colorTo: "green"
sdk: "docker"
app_file: Dockerfile
pinned: true
---

# RealProject

AI Exam Evaluator using OpenEnv + FastAPI

## Features
- Automated grading
- Step/reset/state API
- Multi-level tasks (easy → hard)

## Run locally
uvicorn server.app:app --reload