FROM nvidia/cuda:12.2.0-devel-ubuntu22.04 as base

WORKDIR /src

FROM base as build 

RUN apt-get update && \
    apt-get install -y build-essential python3.10 python3-pip python3-venv && \
    pip install pipx && \
    pipx ensurepath && \
    pipx ensurepath --global && \
    pipx install poetry 
ENV PATH=/root/.local/bin:$PATH
# Poetry setup 
RUN poetry config cache-dir /envs && \
 poetry config virtualenvs.create false 

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install

EXPOSE 8051

CMD exec uvicorn app.server:app --port 7200 --host 0.0.0.0
