FROM spark:3.5.0-python3
LABEL authors="Alex Egorov"

USER root

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /app

USER spark