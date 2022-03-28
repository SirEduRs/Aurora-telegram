FROM python:3.10.4

ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update; \
    apt-get upgrade -y; \
    pip install --upgrade pip; \
    pip install "poetry==1.1.13"; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*;

WORKDIR /bottg/

COPY ./poetry.lock ./pyproject.toml /bottg/

RUN poetry install;
RUN poetry update;

COPY . .

ENTRYPOINT [ "python", "main.py" ]