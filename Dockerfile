FROM python:3-alpine

RUN apk update && \
   apk --no-cache add ca-certificates bash

# install requirements
ADD requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# install assets
ADD assets/ /opt/resource/
