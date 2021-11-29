#!/bin/ash
mkdir -p /eth/geth

test ! -z "${rpccorsdomain}" && CORS_OPT="--http.corsdomain ${rpccorsdomain}"
test ! -z "${rpcvhosts}" && VHOST_OPT="--http.vhosts ${rpcvhosts}"
test ! -z "${maxpeers}" && PEERS_OPT="--maxpeers ${maxpeers}"

GETH_CMD="geth \
--http \
--http.addr 0.0.0.0 \
--http.port 8545 \
${CORS_OPT} \
--datadir /eth \
--port 30303 \
--http.api admin,debug,miner,txpool,eth,net,web3,istanbul,personal \
${VHOST_OPT} \
--networkid 1500002 \
--nat any \
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
  ps -ef | grep -v grep | grep "geth --http" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "$0: geth Running."
    break
  fi
done

function trap_sigint() {
  echo "$0: geth Shutdown."
  PID=$(ps -ef | grep "geth --http" | grep -v grep | awk '{print $1}')
  kill -SIGINT ${PID}
  while :; do
    ps -ef | grep -v grep | grep "geth --http" > /dev/null 2>&1
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
