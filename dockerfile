from python:3.9 as dev

workdir /app

copy ./ .
run pip install --no-cache-dir --upgrade -r reqs.txt

cmd ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

