# 🚀 Connect to ibet testnet

**ibet testnet** is a network open to any developer who uses the ibet (or ibet for Fin) network.
All developer can connect it . 
All developer can do the development and testing.

### 3 types of nodes

The ibet testnet consists of 3 types of nodes.

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

Node key settings are also configurable through environment variables.

* `nodekey` Path to the legacy node key file inside the container  
* `nodekeyhex` Legacy node key as hex string  
* `nodekeysource` Node key source (`file` or `aws-sm`)  
* `nodekeydecryption` Node key decryption (`none` or `aws-kms`)  
* `nodekey_aws_secret_name` AWS Secrets Manager secret name or ARN  
* `nodekey_aws_secret_version_id` AWS secret version ID. When `nodekeysource=aws-sm`, this is required if `nodekey_aws_secret_version_stage` is not set.  
* `nodekey_aws_secret_version_stage` AWS secret version stage, such as `AWSCURRENT`. When `nodekeysource=aws-sm`, this is required if `nodekey_aws_secret_version_id` is not set. Exactly one of `nodekey_aws_secret_version_id` or `nodekey_aws_secret_version_stage` must be specified when `nodekeysource=aws-sm`.  
* `nodekey_aws_kms_key_id` AWS KMS key ID or alias, required when `nodekeydecryption=aws-kms`  
* `nodekey_aws_kms_encryption_algorithm` Optional KMS encryption algorithm override, such as `RSAES_OAEP_SHA_256`  

When `nodekey` or `nodekeyhex` is specified, the legacy configuration takes precedence and no additional AWS configuration is required.

## 2. Start/Stop Validator node

### Set up

Pull docker image for validator nodes.
```
$ docker pull ghcr.io/boostryjp/ibet-testnet/validator:{version}
```

Make a volume mount directory for the docker container.
```
$ mkdir -p {mount_directory}/geth
```

Move `genesis.json` and `static-nodes.json` for the Validator network.
- {mount_directory}/genesis.json
- {mount_directory}/genesis.json_init
- {mount_directory}/geth/static-nodes.json

### Start validator node

Initialize the node. You need to run only the first time.
```
$ docker run --rm --name validatorInit -e PRIVATE_CONFIG=ignore -v {mount_directory}:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:{version} \
    geth --datadir /eth init /eth/genesis.json_init
```

Finally, start the node as follows.
```
$ docker run -d --name validator -e PRIVATE_CONFIG=ignore -e nodekeyhex={nodekey} -v {mount_directory}:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:{version} run.sh 
```

To load the validator node key from AWS Secrets Manager instead, start it as follows.
```
$ docker run -d --name validator -e PRIVATE_CONFIG=ignore \
    -e nodekeysource=aws-sm \
    -e nodekeydecryption=aws-kms \
    -e nodekey_aws_secret_name={secret_name_or_arn} \
    -e nodekey_aws_secret_version_stage=AWSCURRENT \
    -e nodekey_aws_kms_key_id={kms_key_id_or_alias} \
    -v {mount_directory}:/eth \
    ghcr.io/boostryjp/ibet-testnet/validator:{version} run.sh
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
$ docker pull ghcr.io/boostryjp/ibet-testnet/general:{version}
```

Make a volume mount directory for the docker container.
```
$ mkdir -p {mount_directory}/geth
```

Move `genesis.json` and `static-nodes.json`. 
- {mount_directory}/genesis.json
- {mount_directory}/genesis.json_init
- {mount_directory}/geth/static-nodes.json

Set the boot node to be connected in the static-nodes.json file.
If a Bridge node is to be connected, the Validator node must be set as the connection node; 
if a General node, the Bridge node must be set as the connection node.

### Start node

Initialize the node. You need to run only the first time.
```
$ docker run --rm --name generalInit -e PRIVATE_CONFIG=ignore -v {mount_directory}:/eth \
    ghcr.io/boostryjp/ibet-testnet/general:{version} \
    geth --datadir /eth init /eth/genesis.json_init
```

Finally, start the node as follows.
```
$ docker run -d --name general -e PRIVATE_CONFIG=ignore -v {mount_direcotry}:/eth \
    ghcr.io/boostryjp/ibet-testnet/general:{version} run.sh 
```

The same AWS node key settings can be used for Bridge and General nodes as well.

### Stop node 
When stopping a node, simply stop the container.
```
$ docker stop general
```
