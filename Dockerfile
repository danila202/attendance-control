FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app
COPY ./osa /app

EXPOSE 8000

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
