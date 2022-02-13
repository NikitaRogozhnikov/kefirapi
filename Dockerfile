FROM python:3.8-slim-buster

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./kefirapi

EXPOSE 5000

CMD ["python", "kefirapi/runner.py"]
