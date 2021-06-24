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
    git checkout v21.1.0
COPY freezer.go /work/quorum/core/rawdb/
RUN cd quorum/ && \
    make geth bootnode && \
    mv build/bin/geth /usr/local/bin && \
    mv build/bin/bootnode /usr/local/bin

FROM alpine:3.13.0

RUN apk add --no-cache ca-certificates

COPY --from=builder \
         /usr/local/bin/geth \
         /usr/local/bin/bootnode \
     /usr/local/bin/

COPY run.sh /run.sh
COPY healthcheck.sh /healthcheck.sh

EXPOSE 30303 30303/udp 8545

STOPSIGNAL SIGINT
CMD ["/run.sh"]
HEALTHCHECK --interval=30s CMD /healthcheck.sh
