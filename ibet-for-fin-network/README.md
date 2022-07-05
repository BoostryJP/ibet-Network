# 🚀 Connect to ibet for Fin

**ibet for Fin** is a network that is primarily open to financial institutions only.
Products that require the intermediation of licensed financial institutions in the secondary market are distributed.  

### 3 types of nodes

The ibet for Fin network consists of 3 types of nodes.

#### Validator
- Verify the integrity of transactions. 
- The Validator nodes are connected to each other through an internal network, and the Bridge nodes are the only nodes that are externally connected.

#### Bridge
- It exists as a proxy to connect the Validator and General nodes. 
- It is itself a full node; it connects to the General node via the Internet. 

#### General
- A node held by consortium members and used by them from their own services.
- It is a full node and is used to send transactions and to reference blockchain data.

---

## 1. Common settings

Common to all three types of nodes, you need to set the following environment variables.

* `PRIVATE_CONFIG` Only "ignore" can be set  
* `rpccorsdomain` Comma separated list of domains from which to accept cross origin requests (default:*)  
* `rpcvhosts` Comma separated list of virtual hostnames from which to accept requests (default: "localhost")  
* `maxpeers` Maximum number of network peers (network disabled if set to 0) (default: 50)  

## 2. Start/Stop Validator node

### Set up

Pull docker image for validator nodes.
```
$ docker pull ghcr.io/boostryjp/ibet-fin-network/validator:{version}
```

Make a volume mount directory for the docker container.
```
$ mkdir -p {mount_directory}/geth
```

Move `genesis.json` and `static-nodes.json` for the validator network as follows.
- {mount_directory}/genesis.json
- {mount_directory}/geth/static-nodes.json

### Start validator node 

Initialize the node. You need to run only the first time.
```
$ docker run --name validatorInit -e PRIVATE_CONFIG=ignore -v {mount_directory}:/eth \
    ghcr.io/boostryjp/ibet-fin-network/validator:{version} \
    geth --datadir /eth --nousb init /eth/genesis.json
```

Finally, start the node as follows.
```
$ docker run -d --name validator -e PRIVATE_CONFIG=ignore -v {mount_directory}:/eth \
    ghcr.io/boostryjp/ibet-fin-network/validator:{version} run.sh 
```

### Stop validator node 

When stopping a node, simply stop the container.
```
$ docker stop validator
```

## 3. Start/Stop Bridge or General node

### Set up

Pull docker image for general nodes.
Bridge node image is exactly the same as that of the General node.
```
$ docker pull ghcr.io/boostryjp/ibet-fin-network/general:{version}
```

Make a volume mount directory for the docker container.
```
$ mkdir -p {mount_directory}/geth
```

Move `genesis.json` and `static-nodes.json` as follows. 
- {mount_directory}/genesis.json
- {mount_directory}/geth/static-nodes.json

Set the boot node to be connected in the static-nodes.json file.
If a Bridge node is to be connected, the Validator node must be set as the connection node; 
if a General node, the Bridge node must be set as the connection node.

### Start node

Initialize the node. You need to run only the first time.
```
$ docker run --name generalInit -e PRIVATE_CONFIG=ignore -v {mount_directory}:/eth \
    ghcr.io/boostryjp/ibet-fin-network/general:{version} \
    geth --datadir /eth --nousb init /eth/genesis.json
```

Finally, start the node as follows.
```
$ docker run -d --name general -e PRIVATE_CONFIG=ignore -v {mount_direcotry}:/eth \
    ghcr.io/boostryjp/ibet-fin-network/general:{version} run.sh 
```

### Stop node 
When stopping a node, simply stop the container.
```
$ docker stop general
```
