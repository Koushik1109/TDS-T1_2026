FROM python:3.11-slim

# Requirement for Spaces: non-root user with UID 1000
# See https://huggingface.co/docs/hub/spaces-sdks-docker
RUN useradd -m -u 1000 user

WORKDIR /app

# Copy and install dependencies
COPY --chown=user requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY --chown=user . .

# Port configuration
ENV APP_PORT=7073
EXPOSE 7073

# Switch to non-root user UID 1000
USER user

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $APP_PORT"]
