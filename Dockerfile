FROM python:3.10-slim AS base

WORKDIR /app

ENV LANG=C.UTF-8 \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1	\
	VENV="/opt/venv" \
	APPUSER=appuser \
	PATH="${VENV}/bin:$PATH"

FROM base as builder

COPY requirements.txt .

RUN apt-get update \
	&& apt-get install -y build-essential \
    && python -m venv ${VENV} \
	&& . ${VENV}/bin/activate \
	&& pip install --upgrade pip \
	&& pip install -r requirements.txt

FROM base as runner

COPY --from=builder ${VENV} ${VENV}
RUN apt-get update \
	&& apt-get install -y mosquitto-clients \
    && apt-get clean

ARG GPIO_ID
ARG BROKER_IP
ARG BROKER_PORT
ARG TOPIC
ARG MESSAGE_HIGH
ARG MESSAGE_LOW
ARG USER
ARG PASSWORD

ENV GPIO_ID=${GPIO_ID}
ENV BROKER_IP=${BROKER_IP}
ENV BROKER_PORT=${BROKER_PORT}
ENV TOPIC=${TOPIC}
ENV MESSAGE_HIGH=${MESSAGE_HIGH}
ENV MESSAGE_LOW=${MESSAGE_LOW}
ENV USER=${USER}
ENV PASSWORD=${PASSWORD}

ENV PATH="${VENV}/bin:$PATH"

COPY gpio_switch.py .

RUN chgrp -R 0 /app \
	&& chmod -R g=u /app \
	&& groupadd -r ${APPUSER} \
	&& useradd -r -g ${APPUSER} ${APPUSER} \
	&& chown -R ${APPUSER}:${APPUSER} /app \
	&& usermod -d /app ${APPUSER}

ENTRYPOINT /opt/venv/bin/python3 gpio_switch.py \
            --gpio ${GPIO_ID} \
            --broker_ip ${BROKER_IP} \
            --broker_port ${BROKER_PORT} \
            --topic ${TOPIC} \
            --message_high ${MESSAGE_HIGH} \
            --message_low ${MESSAGE_LOW} \
            --user ${USER} \
            --password ${PASSWORD}
