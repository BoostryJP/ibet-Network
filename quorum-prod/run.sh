#!/bin/bash
mkdir -p /eth/geth

geth --datadir "/eth" init "/eth/genesis.json"

geth \
--rpc \
--rpcaddr "0.0.0.0" \
--rpcport "8545" \
--rpccorsdomain "*" \
--datadir "/eth" \
--port "30303" \
--rpcapi "db,eth,net,web3,istanbul,personal" \
--networkid "1500002" \
--nat "any" \
--nodekeyhex $nodekeyhex \
--mine \
--syncmode "full" \
--gasprice 0 \
--verbosity 2
