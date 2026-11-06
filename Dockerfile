FROM alpine:3.12

WORKDIR /myfirstpipeline

ADD . /myfirstpipeline

RUN apk add python3

