FROM spark:3.5.0-python3
LABEL authors="Alex Egorov"

USER root

RUN pip install scikit-learn loguru
COPY src /app

USER spark