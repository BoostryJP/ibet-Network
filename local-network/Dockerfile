FROM golang:1.13-alpine as builder

WORKDIR /work

RUN apk add --no-cache && \
    apk add git \
            make \
            gcc \
            musl-dev \
            linux-headers

RUN git clone https://github.com/jpmorganchase/quorum.git && \
    cd quorum/ && \
    git checkout v2.7.0
COPY freezer.go /work/quorum/core/rawdb/
RUN cd quorum/ && \
    make geth bootnode && \
    mv build/bin/geth /usr/local/bin && \
    mv build/bin/bootnode /usr/local/bin

FROM alpine:3.12.0

RUN apk add --no-cache ca-certificates

COPY --from=builder \
    /usr/local/bin/geth \
    /usr/local/bin/bootnode \
    /usr/local/bin/

EXPOSE 30303/tcp 30303/udp 30304/udp 8545/tcp 8546/tcp

CMD ["/bin/sh"]
