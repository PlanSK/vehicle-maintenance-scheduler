# === Stage 1: Build Dependencies (Builder) ===
FROM python:3.12-alpine AS builder

WORKDIR /usr/src/webapp

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for building Python packages
RUN apk add --no-cache gcc python3-dev musl-dev mariadb-dev

RUN pip install --no-cache-dir --upgrade pip

# Copy ONLY requirements.txt to maximize Docker layer caching
COPY ./requirements.txt .

# Build wheels (compiled once and cached)
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/webapp/wheels -r requirements.txt


# === Stage 2: Final Production Image ===
FROM python:3.12-alpine

# Create a system group and user in a single command
RUN addgroup -S implementer && adduser -S implementer -G implementer

ENV HOME=/home/implementer
ENV APP_HOME=/home/implementer/web

# Create all required directories in a single command
RUN mkdir -p $APP_HOME/staticfiles $APP_HOME/mediafiles $APP_HOME/db
WORKDIR $APP_HOME

# Install only the runtime client package required for MariaDB/MySQL
RUN apk add --no-cache mariadb-connector-c-dev

# Copy wheels from the builder stage and install them
COPY --from=builder /usr/src/webapp/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy and configure entrypoint before copying the source code to preserve cache
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh && chmod +x entrypoint.sh

# Copy the project source code
COPY . $APP_HOME

# Change ownership of the application directory to the non-root user
RUN chown -R implementer:implementer $APP_HOME

USER implementer

ENTRYPOINT ["./entrypoint.sh"]
