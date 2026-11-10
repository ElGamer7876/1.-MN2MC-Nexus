# Explicit web runtime: avoids the upstream minecraft-protocol package.json autodetection.
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
WORKDIR /app
COPY worker/requirements.txt worker/requirements.txt
RUN python -m pip install --no-cache-dir -r worker/requirements.txt
COPY worker/app worker/app
COPY site site
RUN useradd --system --uid 10001 --create-home nexus
USER nexus
EXPOSE 8080
CMD ["sh", "-c", "exec uvicorn app.main:app --app-dir worker --host 0.0.0.0 --port $PORT"]
