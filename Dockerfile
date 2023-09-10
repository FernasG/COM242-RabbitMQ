ARG PYTHON_VERSION=3.10.12
ARG PIP_VERSION=23.1

FROM python:${PYTHON_VERSION}

ARG PIP_VERSION
ENV PIP_VERSION ${PIP_VERSION}

RUN apt update

COPY requirements.txt .

RUN python3 -m pip install --upgrade 'pip>=${PIP_VERSION}' \
    && python3 -m pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD ["python3", "server.py"]