FROM python:3.12-slim AS python-base

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false\
    ENV="prod"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY . ./

RUN --mount=type=cache,target=/root/.cache \
    poetry install --without=dev --no-root

EXPOSE 5151
ENTRYPOINT ["python", "-m", "twitchrewards.server"]