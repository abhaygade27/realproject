---
title: Real Project Environment
emoji: "🤖"
colorFrom: "blue"
colorTo: "green"
app_file: "app.py"  # if your main app file is app.py
sdk: "gradio"        # or "streamlit", depending on your app
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