FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MODULE_NAME=app.main
ENV VARIABLE_NAME=app
ENV PORT=80

EXPOSE $PORT

CMD ["sh", "-c", "uvicorn $MODULE_NAME:$VARIABLE_NAME --host 0.0.0.0 --port $PORT"]