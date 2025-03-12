# Use a slim Python base image for smaller size
FROM python:3.10-slim-bookworm as base

# Set working directory
WORKDIR /src

# Install dependencies in a separate build stage
FROM base as build

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

# Install pipx & Poetry in a single step to reduce layers
RUN pip install --no-cache-dir pipx && \
    pipx install poetry && \
    poetry config cache-dir /envs && \
    poetry config virtualenvs.create false

# Ensure pipx-installed binaries are available in PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy and install dependencies
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi

# Copy application files separately to leverage Docker cache
COPY . .

# Use a lightweight runtime stage
FROM base

# Copy installed dependencies from build stage
COPY --from=build /src /src

# Set working directory again
WORKDIR /src

# Expose necessary ports
EXPOSE 8000

# Set the entrypoint for the Streamlit app
CMD ["streamlit", "run", "Welcome.py", "--server.port", "8000"]
