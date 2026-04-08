🚀 OpenEnv AI Exam Evaluator
An AI-powered evaluation environment built using OpenEnv, where an agent automatically grades student answers based on a defined rubric.

📌 Project Overview
This project simulates a real-world exam evaluation system where:

An AI agent evaluates answers

Scores are assigned from 0.0 to 1.0

Environment follows standard OpenEnv API:

reset()

step(action)

state()

⚙️ Features
✅ Automated grading system

✅ Multiple difficulty levels (Easy → Medium → Hard)

✅ Reward-based evaluation (0.0 – 1.0)

✅ REST API using FastAPI

✅ Dockerized for deployment

✅ Compatible with Hugging Face Spaces

📂 Project Structure
Code
OPENENV/
├── server/
│   ├── app.py              # FastAPI server endpoints
│   ├── environment.py      # ExamEnv class implementing reset/step/state
│   └── __init__.py
│
├── dataset.json            # Questions & answers (easy/medium/hard)
├── Grader.py               # Multi-case grader
├── inference.py            # Baseline inference script
├── models.py               # Typed Pydantic models (Observation, Action, Reward)
├── Openenv.yaml            # OpenEnv specification file
├── pyproject.toml          # Python project metadata + dependencies
├── Dockerfile              # Container build
├── README.md               # Documentation
└── validate-submission.sh  # Pre-validation script
🏆 Reward Function
Reward is calculated as:

Code
reward = max(0, 1 - (|agent_score - expected_score| / 10))
This produces partial progress signals (e.g., 0.4, 0.7, 1.0) instead of binary pass/fail, encouraging agents to approximate rubric alignment.

🔧 Installation
bash
git clone https://github.com/<your-username>/OPENENV.git
cd OPENENV
pip install -e .
▶️ Run Locally
bash
uvicorn server.app:app --host 0.0.0.0 --port 8000
🧪 Usage
Run baseline inference
bash
python inference.py
Run grader
bash
python Grader.py
🐳 Docker Setup
Build Image
bash
docker build -t openenv-evaluator .
Run Container
bash
docker run -p 8000:8000 openenv-evaluator
🌐 Deployment (Hugging Face Spaces)
Create a new Space (Docker type)

Upload project files

Ensure:

Dockerfile exists

Port = 8000

Wait for build to complete

✅ Prevalidation
Run the validation script:

bash
./validate-submission.sh https://<username>-OPENENV.hf.space ./OPENENV
📜 License
MIT License