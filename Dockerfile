FROM python:3.14-slim

WORKDIR /async_combinator

RUN pip install poetry
COPY poetry.toml pyproject.toml poetry.lock README.md ./
COPY async_combinator async_combinator/
RUN poetry install --no-interaction --no-ansi

ENTRYPOINT ["tail", "-f", "/dev/null"]
