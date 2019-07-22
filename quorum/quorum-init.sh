#!/bin/bash
set -u
set -e

# 引数チェック
MESSAGE='Usage: quorum-init.sh <node-label>
                node-label: A ~ D'

if ( [ $# -ne 1 ] ); then
    echo "$MESSAGE"
    exit
fi

# datadirの初期化
sudo rm -rf qdata
mkdir -p qdata/{logs,keys}
mkdir -p qdata/dd/geth
mkdir -p qdata/dd/keystore


# 変数
node_label="$1"
pwd=`pwd`

# 設定copy
cp istanbul-genesis.json qdata/genesis.json
cp static-nodes.json qdata/dd/static-nodes.json
cp static-nodes.json qdata/dd/permissioned-nodes.json
cp tmconf/tm${node_label}.conf qdata/tm.conf
cp pass.txt qdata/pass.txt

# key copy
cp keys/nodekey${node_label} qdata/dd/geth/nodekey
#cp keys/key${node_label}.json qdata/dd/keystore/acckey
cp keys/tm${node_label}.key qdata/keys/tm.key
cp keys/tm${node_label}.pub qdata/keys/tm.pub

# docker run時の実行shのcopy
cp start-node.sh qdata/start-node.sh

# geth init
docker run --rm --name quorum -v $pwd/qdata:/qdata quorum /usr/local/bin/geth --datadir /qdata/dd init /qdata/genesis.json

# 5秒待つ
sleep 5