FROM ubuntu:latest
LABEL authors="matveyfedorov"

ENTRYPOINT ["top", "-b"]