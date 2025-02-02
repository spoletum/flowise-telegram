FROM python:3.13-rc-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock README.md ./
COPY main.py .

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies (only production)
RUN poetry install --only main --no-interaction --no-ansi --no-root

# Run the bot
CMD ["python", "main.py"]
