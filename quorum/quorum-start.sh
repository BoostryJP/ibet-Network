#!/bin/bash
set -u
set -e

# 変数
pwd=`pwd`

# geth 起動
docker run --rm -d --name quorum -v $pwd/qdata:/qdata -p 9000:9000 -p 21000:21000 -p 21000:21000/udp -p 8545:8545 -e NODE_TYPE=validator quorum