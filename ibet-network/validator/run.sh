#!/bin/ash
mkdir -p /eth/geth

geth --datadir "/eth" --nousb init "/eth/genesis.json"

test ! -z "${rpccorsdomain}" && CORS_OPT="--rpccorsdomain ${rpccorsdomain}"
test ! -z "${rpcvhosts}" && VHOST_OPT="--rpcvhosts ${rpcvhosts}"
test ! -z "${maxpeers}" && PEERS_OPT="--maxpeers ${maxpeers}"

GETH_CMD="geth \
--rpc \
--rpcaddr 0.0.0.0 \
--rpcport 8545 \
${CORS_OPT} \
--datadir /eth \
--port 30303 \
--rpcapi admin,debug,miner,txpool,db,eth,net,web3,istanbul,personal \
${VHOST_OPT} \
--networkid 1500002 \
--nat any \
--nodekeyhex $nodekeyhex \
--mine \
--syncmode full \
--miner.gasprice 0 \
--verbosity 2 \
--nodiscover \
--allow-insecure-unlock \
--miner.gastarget 800000000 \
${PEERS_OPT} \
--nousb"

ash -c "nohup ${GETH_CMD//\*/\\\*} > /dev/stdout 2>&1 &"

for i in $(seq 1 300); do
  sleep 1
  ps -ef | grep -v grep | grep "geth --rpc" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "$0: geth Running."
    break
  fi
done


function trap_sigint() {
  echo "$0: geth Shutdown."
  PID=$(ps -ef | grep "geth --rpc" | grep -v grep | awk '{print $1}')
  kill -SIGINT ${PID}
  while :; do
    ps -ef | grep -v grep | grep "geth --rpc" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
      break
    fi
    sleep 1
  done
  exit 0
}
trap trap_sigint INT

while :; do
  sleep 5
done

