ARG PYVERSION=py39
FROM baseten/baseten-server-gpu-base-$PYVERSION:latest

COPY ./src/server_requirements.txt server_requirements.txt
RUN pip install -r server_requirements.txt

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# BaseTen specific build arguments and environment variables
ARG RUNTIME_ENV
ARG SENTRY_URL
ENV RUNTIME_ENV=$RUNTIME_ENV
ENV SENTRY_URL=$SENTRY_URL

ARG MODEL_CLASS
ARG MODEL_CLASS_DEFINITION_FILE

ENV MODEL_CLASS_NAME=$MODEL_CLASS
ENV MODEL_CLASS_FILE=$MODEL_CLASS_DEFINITION_FILE
ENV PORT 8080
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY ./src .
COPY ./config.yaml config.yaml

CMD exec python3 inference_server.py
