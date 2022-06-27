#!/bin/ash
mkdir -p /eth/geth

echo '{"config":{"byzantiumBlock":3,"chainId":2017,"homesteadBlock":1,"eip150Block":2,"eip150Hash":"0x0000000000000000000000000000000000000000000000000000000000000000","eip155Block":3,"eip158Block":3,"istanbul":{"epoch":30000,"policy":0,"testQBFTBlock":'${testQBFTBlock}'}},"nonce":"0x0","timestamp":"0x5ad86387","extraData":"0x0000000000000000000000000000000000000000000000000000000000000000f89af8549447a847fbdf801154253593851ac9a2e7753235349403ee8c85944b16dfa517cb0ddefe123c7341a5349435d56a7515e824be4122f033d60063d035573a0c94c25d04978fd86ee604feb88f3c635d555eb6d42db8410000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c0","gasLimit":"0x2faf0800","difficulty":"0x1","mixHash":"0x63746963616c2062797a616e74696e65206661756c7420746f6c6572616e6365","coinbase":"0x0000000000000000000000000000000000000000","alloc":{"03ee8c85944b16dfa517cb0ddefe123c7341a534":{"balance":"0x446c3b15f9926687d2c40534fdb564000000000000"},"35d56a7515e824be4122f033d60063d035573a0c":{"balance":"0x446c3b15f9926687d2c40534fdb564000000000000"},"47a847fbdf801154253593851ac9a2e775323534":{"balance":"0x446c3b15f9926687d2c40534fdb564000000000000"},"c25d04978fd86ee604feb88f3c635d555eb6d42d":{"balance":"0x446c3b15f9926687d2c40534fdb564000000000000"}},"number":"0x0","gasUsed":"0x0","parentHash":"0x0000000000000000000000000000000000000000000000000000000000000000"}' > /eth/genesis.json
echo '["enode://6204d2b6d844adf9dd23f47027b29b1e39b08c70b8ec05f82a8037f1676c058fe80035b42f32c649cc47347889abfe7732139b9f3f243ea91f990d2d72bb87bd@172.16.239.10:30303?discport=0","enode://a573feff0859205b566385aaf85f4c858dfe4ebb07ec862a2d03e117b3e39d8220aaf1d58750440ad844ddcb623f6becc9ba07fc27db4d30cdf689f15a9b1462@172.16.239.11:30303?discport=0","enode://76b750a2a0c92d2411e4793c714a85cf01e527c7a77f70548e7f363feaf8320039cd0f2eb48235c022d39df44ec06c96060f5c25caeec8a1960a356ebd5473a1@172.16.239.12:30303?discport=0","enode://f53fff2c7ed693b627d4389b92b6d94a11b91f167193a5d31320a2b35fb752f79b3aed7dcc61961bc00b397fdf8729eb797a0b28d6c538d51232164432b67f80@172.16.239.13:30303?discport=0"]' > /eth/geth/static-nodes.json
geth --datadir "/eth" init "/eth/genesis.json"

GETH_CMD="geth \
--datadir /eth \
--identity ${identity} \
--nodekeyhex ${nodekeyhex} \
--port 30303 \
--networkid 2017 \
--nat any \
--http \
--http.addr 0.0.0.0 \
--http.port 8545 \
--http.api admin,eth,net,web3,istanbul,personal,txpool,debug \
--http.corsdomain ${rpccorsdomain} \
--http.vhosts ${rpcvhosts} \
--allow-insecure-unlock \
--debug \
--metrics \
--mine \
--syncmode full \
--miner.gasprice 0 \
--miner.gastarget 800000000 \
--cache ${cache} \
--nousb"

ash -c "nohup ${GETH_CMD//\*/\\\*} > /dev/stdout 2>&1 &"

for i in $(seq 1 300); do
  sleep 1
  ps -ef | grep -v grep | grep "geth --datadir" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "$0: geth Running."
    break
  fi
done

function trap_sigint() {
  echo "$0: geth Shutdown."
  PID=$(ps -ef | grep "geth --datadir" | grep -v grep | awk '{print $1}')
  kill -SIGINT ${PID}
  while :; do
    ps -ef | grep -v grep | grep "geth --datadir" > /dev/null 2>&1
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
