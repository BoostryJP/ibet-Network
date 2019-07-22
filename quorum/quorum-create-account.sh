#!/bin/bash
set -u
set -e

# 変数
pwd=`pwd`

# geth 起動
docker run --rm --name quorum-create -v $pwd/qdata:/qdata quorum /usr/local/bin/geth account new --datadir /qdata/dd --password /qdata/pass.txt
