FROM python:3.8

WORKDIR /code
COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN pip install poetry
RUN poetry install

COPY . /code

CMD ["poetry", "run", "gunicorn", "main:app", "--bind", "0.0.0.0:8120"]