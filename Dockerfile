FROM python:3.10-slim-buster as builder

WORKDIR /nsjail

RUN apt-get -y update \
    && apt-get install -y \
        bison \
        flex \
        g++ \
        gcc \
        git \
        libprotobuf-dev \
        libnl-route-3-dev \
        make \
        pkg-config \
        protobuf-compiler \
        gcc \
        libnl-route-3-200 \
        libprotobuf17 \
        python3-venv 
        
RUN git clone https://github.com/google/nsjail.git .
RUN make

FROM python:3.10-slim-buster as base

ENV PATH=/root/.local/bin:$PATH

RUN apt-get -y update \
    && apt-get install -y \
        gcc \
        libnl-route-3-200 \
        libprotobuf17 \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /nsjail/nsjail /usr/sbin/
RUN chmod +x /usr/sbin/nsjail

COPY requirements.txt /bot/
WORKDIR /bot

RUN python3 -m venv .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["bot.py"]

COPY . /bot
WORKDIR /bot

ARG git_sha="development"
ENV GIT_SHA=$git_sha
ENV BOT_TOKEN=""