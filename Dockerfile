FROM alpine
MAINTAINER tom@tkw01536.de

# Add our app and cd into /app/
ADD getRECd-backend/ /app/
WORKDIR /app/

# Install python3 end deps
RUN apk add --no-cache python3 \
  && apk add --no-cache --virtual build-dependencies libffi-dev openssl-dev python3-dev py3-pip build-base \
  && pip3 install --upgrade pip \
  && pip3 install -r requirements.txt \
  && apk del build-dependencies

EXPOSE 8080

# To ensure that all the variables are set
ENV HOST "0.0.0.0"

# Variables to be set by user
# ENV SPOTIFY_CLIENT_ID
# ENV SPOTIFY_CLIENT_SECRET
# ENV IBM_USER
# ENV IBM_PASS

CMD python3 server.py