FROM python:3.12-slim

# Set uv
RUN pip install uv

# Set the working directory
WORKDIR /usr/src/app/tg-notify-bot

# Copy the dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv pip install . --system

# Copy the project files
COPY . .

# Make the startup script executable
RUN chmod +x ./docker-entrypoint.sh

# Specify the startup script as the entry point
ENTRYPOINT ["./docker-entrypoint.sh"]