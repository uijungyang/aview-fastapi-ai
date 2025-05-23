FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 33333 37373

CMD ["sh", "-c", "python3 -m app.main"]
