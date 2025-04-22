FROM python:3.12-slim

COPY ./app /app/app
COPY requirements.txt /app
WORKDIR /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 33333

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "33333"]
