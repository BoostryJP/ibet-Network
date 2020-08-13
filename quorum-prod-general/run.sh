#!/bin/ash
mkdir -p /eth/geth

geth --datadir "/eth" --nousb init "/eth/genesis.json"

test ! -z "${rpccorsdomain}" && CORS_OPT="--rpccorsdomain \"${rpccorsdomain}\""
geth \
--rpc \
--rpcaddr "0.0.0.0" \
--rpcport "8545" \
${CORS_OPT} \
--datadir "/eth" \
--port "30303" \
--rpcapi "admin,debug,miner,txpool,db,eth,net,web3,istanbul,personal" \
--networkid "1500002" \
--nat "any" \
--miner.gasprice 0 \
--verbosity 2 \
--nodiscover \
--allow-insecure-unlock \
--nousb

