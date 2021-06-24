# Connect to the ibet testnet

`ibet testnet` is a network open to any developer who uses the ibet (or ibet for Fin) network.
All developer can connect it . 
All developer can do the development and testing.

**3 types of nodes**

The ibet testnet consists of 3 types of nodes.

1. `Validator` - Verify the integrity of transactions.  
2. `Bridge` - Connect Validator and General nodes.  
3. `General` - Member companies use it. It sends transactions and refer the blockchain data.  

## 1. Common settings

### Environment variable

* `PRIVATE_CONFIG` Only "ignore" can be set  
* `rpccorsdomain` Comma separated list of domains from which to accept cross origin requests (default:*)  
* `rpcvhosts` Comma separated list of virtual hostnames from which to accept requests (default: "localhost")  
* `maxpeers` Maximum number of network peers (network disabled if set to 0) (default: 50)  

## 2. How to start/stop `Validator` node

### start validator node 

```bash
$ docker pull ghcr.io/boostryjp/ibet-testnet/validator:v1.1.0
$ git clone https://github.com/BoostryJP/ibet-Network.git
$ cd ibet-Network/test-network/validator
$ docker run --name validatorInit -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:v1.1.0 \
    geth --datadir /eth --nousb init /eth/genesis.json_init
$ docker run -d --name validator -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:v1.1.0 run.sh 
```

### stop validator node 

```bash
$ docker stop validator
```

## 3. How to start/stop `Bridge` node

### start bridge node

```bash
$ docker pull ghcr.io/boostryjp/ibet-testnet/general:v1.1.0
$ git clone https://github.com/BoostryJP/ibet-Network.git
$ cd ibet-Network/test-network/general
$ cp static-nodes-bridge.json ./geth/static-nodes.json
$ docker run --name bridgeInit -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/general:v1.1.0 \
    geth --datadir /eth --nousb init /eth/genesis.json_init
$ docker run -d --name bridge -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/general:v1.1.0 run.sh 
```

### stop bridge node 

```bash
$ docker stop bridge
```

## 4. How to start/stop `General` node

### start general node

```bash
$ docker pull ghcr.io/boostryjp/ibet-testnet/general:v1.1.0
$ git clone https://github.com/BoostryJP/ibet-Network.git
$ cd ibet-Network/test-network/general
$ cp static-nodes-general.json ./geth/static-nodes.json
$ docker run --name generalInit -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/general:v1.1.0 \
    geth --datadir /eth --nousb init /eth/genesis.json_init
$ docker run -d --name general -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/general:v1.1.0 run.sh 
```

### stop general node 

```bash
$ docker stop general
```
