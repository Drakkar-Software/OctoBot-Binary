FROM python:3.8-slim-buster

ARG GH_REPO
ARG OCTOBOT_GH_REPO
ARG OCTOBOT_DEFAULT_BRANCH
ARG OCTOBOT_REPOSITORY_DIR
ARG NLTK_DATA
ARG BUILD_ARCH

WORKDIR /build

ADD . .
RUN apt-get update \
    && apt-get install  -y --no-install-recommends git gcc libc6
RUN bash build_scripts/unix.sh
