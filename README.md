# ibet-Network

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.1-blue.svg?cacheSeconds=2592000" />
</p>

<img width="33%" align="right" src="https://user-images.githubusercontent.com/963333/130191619-f1f0c342-ab8f-499d-b8f8-52309c13d2cb.png"/>

## Features

[ibet](https://ibet.jp/) is a consortium blockchain built and operated mainly by [BOOSTRY Co., Ltd.](https://boostry.co.jp/).

### 1. Consortium blockchain

ibet is a consortium blockchain. 
It is built using [Quorum](https://consensys.net/quorum/), an OSS blockchain for enterprise. 
Currently, it is being developed only for the Japanese market.

ibet is a consortium blockchain made up of "companies". 
Each company in the consortium builds its own node (non-Validator node) and connects it to the network.

### 2. Two networks

There are two consortium networks, "**ibet**" and "**ibet for Fin**", in compliance with Japanese laws and regulations.
Each of them constitutes its own blockchain network.

Each consortium has its own independent governance and operates according to its own terms of reference and guidelines.

- **ibet** : A network in which any company can participate. Mainly non-financial rights (utility tokens) are distributed.
- **ibet for Fin** : A network in which mainly only financial institutions can participate. Products that require the intermediation of licensed financial institutions in the secondary market are distributed.


## About this repository

This repository manages the network definitions and Quorum node containers (Validator, General) defined by the ibet consortium.

### Repository structure

The network definitions and node definitions for each network are stored in each of the following directories.

- `ibet-network` : ibet production network
- `ibet-for-fin-network` : ibet for Fin production network
- `test-network` : ibet test network
- `local-network` : local network

### Version control policy

The repository of ibet-Network will be version controlled by the following policy.

- Version up of the whole repository is done every 6 months.
- Version up of the Quorum node will be done every 6 months. The version to be adopted in the next update will be decided by consortium agreement.
  - Without a hard fork: Minor version up (e.g. 1.0 -> 1.1)
  - With a hard fork: Major version up (e.g., 1.0 -> 2.0)
- For other urgent fixes, a revision upgrade will be released urgently (e.g., 1.1.0 -> 1.1.1).


## Quorum Version

Currently, ibet is using [v21.1.0](https://github.com/ConsenSys/quorum/releases/tag/v21.1.0) of Quorum.


## How to Join the ibet Network

For more information on how to join the network, please visit the official [ibet website](https://ibet.jp/).


## License

- The go-ethereum library is licensed under the
[GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html), also
included in our repository in the `COPYING.LESSER` file.

- The go-ethereum binaries is licensed under the
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), also included
in our repository in the `COPYING` file.
