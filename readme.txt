This is a common Windows PowerShell issue, not your mistake 👍


#step venv

python -m venv venv

#✅ Fix (Temporary & Safe)Run this command once in the same terminal:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypas

.\venv\Scripts\Activate.ps1

fastapi run krne ke liye:
uvicorn server.app:app --reload

to check the status or it is not loading:
curl http://127.0.0.1:8000/health
# Should return: {"status":"ok"}




python client.py