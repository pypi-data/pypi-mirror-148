ARG PYVERSION=py39
FROM baseten/baseten-server-base-$PYVERSION:latest

COPY ./src/server_requirements.txt server_requirements.txt
RUN pip install -r server_requirements.txt

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# BaseTen specific build arguments and environment variables
ARG RUNTIME_ENV
ARG SENTRY_URL
ENV RUNTIME_ENV=$RUNTIME_ENV
ENV SENTRY_URL=$SENTRY_URL

COPY ./src/server_requirements.txt server_requirements.txt
COPY ./requirements.txt requirements.txt

RUN pip install -r server_requirements.txt
RUN pip install -r requirements.txt

ENV PORT 8080

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./src .

CMD exec python inference_server.py
