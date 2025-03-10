FROM arm64v8/python:3.9

WORKDIR /app

COPY . .

RUN git submodule update --init --recursive

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 33333 37373

CMD ["sh", "-c", "python3 -m app.main"]