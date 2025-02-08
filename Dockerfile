FROM python:3.12-slim

# Set Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /usr/src/app/tg-notify-bot

# Copy the dependency files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root \
    && rm -rf $(poetry env info -p)/.cache/pip

# Copy the project files
COPY . .

# Make the startup script executable
RUN chmod +x ./docker-entrypoint.sh

# Specify the startup script as the entry point
ENTRYPOINT ["./docker-entrypoint.sh"]