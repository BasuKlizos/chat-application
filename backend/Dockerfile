FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000
EXPOSE 5555

CMD [ "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]

