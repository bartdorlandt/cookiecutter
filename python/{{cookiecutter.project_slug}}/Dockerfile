# Using bartdorlandt/nox_poetry image which has multiple python versions installed.
FROM --platform=linux/AMD64 bartdorlandt/nox_poetry:latest

# hadolint ignore=DL3005,DL3008,DL3013
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install --no-install-recommends -y git curl openssl && \
  apt-get autoremove -y && \
  apt-get clean all && \
  rm -rf /var/lib/apt/lists/* && \
  pip --no-cache-dir install --upgrade pip wheel

RUN pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -

# Add poetry install location to the $PATH
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /local
COPY pyproject.toml poetry.lock /local/

RUN poetry config virtualenvs.create false \
  && poetry install --with=dev --no-interaction --no-ansi
