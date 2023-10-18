from python:3.9 as dev

workdir /app
copy reqs.txt .
run pip install --no-cache-dir --upgrade -r reqs.txt
#run pip install watchdog

#cmd ["watchmedo", "shell-command", "--patterns='*.py'", "--command='uvicorn main:app --host 0.0.0.0 --port 80'"]
cmd ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

