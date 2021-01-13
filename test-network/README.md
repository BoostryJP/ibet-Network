# About ibet-for-Fin network
A network in which any developer can participate. All developer can connect it . All deleloper can do the development and testing.    

## 3 kinds of nodes
The test-network has 3 kinds of nodes.  
1. `Validator` : Verify the integrity of transactions
2. `General for bridge` : Connect Validator and General for member.  
3. `General for member` : Member company use it. It send transactions and refer the block chain data.  

### 1. Common elemental 

#### Environment variable

* `PRIVATE_CONFIG` Only "ignore" can be set  
* `rpccorsdomain` Comma separated list of domains from which to accept cross origin requests (default:*)  
* `rpcvhosts` Comma separated list of virtual hostnames from which to accept requests (default: "localhost")  
* `maxpeers` Maximum number of network peers (network disabled if set to 0) (default: 50)  

### 2. How to start/stop Validator node  

#### start validator node 

```
$ docker pull ghcr.io/boostryjp/ibet-testnet/validator:v0.0.1
$ git clone https://github.com/BoostryJP/ibet-Network.git
$ cd ibet-network/validator
$ docker run --name validatorInit -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:v0.0.1 \
    geth --datadir /eth --nousb init /eth/genesis.json_init
$ docker run -d --name validator -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:v0.0.1 run.sh 
```

#### stop validator node 

```
$ docker stop validator
```

### 3. How to start/stop General for bridge node  

#### start General for bridge node 

```
$ docker pull ghcr.io/boostryjp/ibet-testnet/general:v0.0.1
$ git clone https://github.com/BoostryJP/ibet-Network.git
$ cd test-network/generalForBridge
$ docker run --name generalForBridgeInit -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/general:v0.0.1 \
    geth --datadir /eth --nousb init /eth/genesis.json_init
$ docker run -d --name generalForBridge -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:v0.0.1 run.sh 
```

#### stop General for bridge node 

```
$ docker stop generalForBridge
```

### 4. How to start/stop General for member node  

#### start General for member   

```
$ docker pull ghcr.io/boostryjp/ibet-testnet/general:v0.0.1
$ git clone https://github.com/BoostryJP/ibet-Network.git
$ cd test-network/generalForMember
$ docker run --name generalForMemberInit -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/general:v0.0.1 \
    geth --datadir /eth --nousb init /eth/genesis.json_init
$ docker run -d --name generalForBridge -e PRIVATE_CONFIG=ignore -v ./:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:v0.0.1 run.sh 
```

#### stop General for bridge node 

```
$ docker stop generalForMember
```

