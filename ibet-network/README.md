# Connect to the ibet network

`ibet` is a network that any company can join. 
Mainly non-financial rights (utility tokens) are distributed.  

**2 types of nodes**

The ibet network consists of 2 types of nodes.

1. `Validator` - Verify the integrity of transactions
2. `General` - Member companies use it. It sends transactions and refer the blockchain data.  

## 1. Common settings
You need to create a VPC on AWS and connect to ibet network's Validator via VPC Peering.  

### Environment variable

* `PRIVATE_CONFIG` Only "ignore" can be set  
* `rpccorsdomain` Comma separated list of domains from which to accept cross origin requests (default:*)  
* `rpcvhosts` Comma separated list of virtual hostnames from which to accept requests (default: "localhost")  
* `maxpeers` Maximum number of network peers (network disabled if set to 0) (default: 50)  

## 2. How to start/stop `Validator` node  

### start validator node 

```bash
$ docker pull ghcr.io/boostryjp/ibet-network/validator:v1.0.0
$ git clone https://github.com/BoostryJP/ibet-Network.git
$ cd ibet-Network/ibet-network/validator
$ docker run --name validatorInit -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-network/validator:v1.0.0 \
    geth --datadir /eth --nousb init /eth/genesis.json_init
$ docker run -d --name validator -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-network/validator:v1.0.0 run.sh 
```

### stop validator node 

```bash
$ docker stop validator
```

## 3. How to start/stop `General` node  

### start general node

```bash
$ docker pull ghcr.io/boostryjp/ibet-network/general:v1.0.0  
$ git clone https://github.com/BoostryJP/ibet-Network.git
$ cd ibet-Network/ibet-network/general
$ cp ./static-nodes-general.json ./geth/static-nodes.json
$ docker run --name generalInit -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-network/general:v1.0.0 \
    geth --datadir /eth --nousb init /eth/genesis.json_init
$ docker run -d --name general -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-network/general:v1.0.0 run.sh 
```

### stop general node 

```bash
$ docker stop general
```
