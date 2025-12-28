FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG INSTALL_HF=false

WORKDIR /app

COPY requirements.txt requirements-hf.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN if [ "$INSTALL_HF" = "true" ]; then pip install --no-cache-dir -r requirements-hf.txt; fi

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
