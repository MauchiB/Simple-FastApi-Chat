FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install --default-timeout=1000 -r requirements.txt --no-cache-dir
CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]