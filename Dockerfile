FROM ubuntu

WORKDIR /with_ance
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
    
ARG BRANCH=${branch}

RUN echo $BRANCH
RUN git clone -b $BRANCH https://github.com/ysa5347/with_ance_app
RUN ls

# env file은 github workflow에서 생성.
COPY /.env /with_ance/with_ance_app/
COPY /requirements.txt /with_ance/with_ance_app/

RUN pip install -r ./with_ance_app/requirements.txt

ENTRYPOINT sh ./with_ance_app/server.sh