docker-compose run validator-0 geth --datadir /eth --nousb init /eth/genesis.json
docker-compose run validator-1 geth --datadir /eth --nousb init /eth/genesis.json
docker-compose run validator-2 geth --datadir /eth --nousb init /eth/genesis.json
docker-compose run validator-3 geth --datadir /eth --nousb init /eth/genesis.json