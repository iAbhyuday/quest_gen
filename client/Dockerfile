FROM python:3.10-slim-bookworm as base

WORKDIR /src

FROM base as build 

RUN apt-get update && \
    pip install pipx && \
    pipx ensurepath && \
    pipx ensurepath --global && \
    pipx install poetry 
ENV PATH=/root/.local/bin:$PATH
# Poetry setup 
RUN poetry config cache-dir /envs && \
 poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root 

CMD exec streamlit run Welcome.py --server.port 8000
