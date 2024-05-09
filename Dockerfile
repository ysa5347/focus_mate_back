FROM ubuntu

WORKDIR /helloWorld
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get -y upgrade && apt-get -y update
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

RUN apt-get install -y git\
    dnsutils\
    tzdata\
    libmysqlclient-dev\
    screen
RUN apt install -y python3\
    python3-pip
    
ARG BRANCH

RUN echo $BRANCH\
    echo DEBIAN_FRONTEND

RUN git clone -b $BRANCH https://github.com/ysa5347/helloWorld
RUN ls

# env file은 github workflow에서 생성.
COPY /.env /helloWorld/helloWorld/
COPY /requirements.txt /helloWorld/helloWorld/

RUN pip install -r ./helloWorld/requirements.txt

ENTRYPOINT sh ./helloWorld/server.sh