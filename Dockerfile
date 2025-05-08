FROM python:3.12-slim

# Prevents writing .pyc files (__pycache__)
ENV PYTHONDONTWRITEBYTECODE=1
# Forces Python to output logs directly (no buffering) to see logs in real time in Docker / Cloud logs
ENV PYTHONUNBUFFERED=1

ENV DATABASE_URL="sqlite:///./trucks.db"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]