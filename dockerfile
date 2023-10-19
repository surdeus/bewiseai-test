from python:3.9 as dev

workdir /app
# Needs to be copied so we can build the image with
# installed requiriments before the volume is mounted.
# (which is better than copying in my opinion, at least for
# the developpment purposes)
copy reqs.txt .
run pip install --no-cache-dir --upgrade -r reqs.txt

cmd ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
#cmd ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

