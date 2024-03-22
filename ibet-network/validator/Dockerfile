# Build Geth in a stock Go builder container
FROM golang:1.22-alpine as builder

WORKDIR /work

RUN apk add --no-cache make gcc musl-dev linux-headers git

RUN git clone https://github.com/BoostryJP/quorum.git && \
    cd quorum/ && \
    git checkout v2.3.0_beta4
RUN cd quorum/ && \
    make geth bootnode && \
    mv build/bin/geth /usr/local/bin && \
    mv build/bin/bootnode /usr/local/bin

# Pull Geth into a second stage deploy alpine container
FROM alpine:3.17

RUN apk add --no-cache ca-certificates
COPY --from=builder /usr/local/bin/geth /usr/local/bin/
COPY --from=builder /usr/local/bin/bootnode /usr/local/bin/

COPY run.sh /run.sh
COPY healthcheck.sh /healthcheck.sh

EXPOSE 30303 30303/udp 8545

STOPSIGNAL SIGINT
CMD ["/run.sh"]
HEALTHCHECK --interval=30s CMD /healthcheck.sh
