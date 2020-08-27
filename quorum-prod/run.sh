#!/bin/ash
mkdir -p /eth/geth

geth --datadir "/eth" --nousb init "/eth/genesis.json"

test ! -z "${rpccorsdomain}" && CORS_OPT="--rpccorsdomain ${rpccorsdomain}"
GETH_CMD="geth \
--rpc \
--rpcaddr 0.0.0.0 \
--rpcport 8545 \
${CORS_OPT} \
--datadir /eth \
--port 30303 \
--rpcapi admin,debug,miner,txpool,db,eth,net,web3,istanbul,personal \
--rpcvhosts * \
--networkid 1500002 \
--nat any \
--nodekeyhex $nodekeyhex \
--mine \
--syncmode full \
--miner.gasprice 0 \
--verbosity 2 \
--nodiscover \
--allow-insecure-unlock \
--nousb"

ash -c "${GETH_CMD//\*/\\\*}"
