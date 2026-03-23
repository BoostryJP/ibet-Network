<p align="center">
  <img width="33%" src="https://user-images.githubusercontent.com/963333/130191619-f1f0c342-ab8f-499d-b8f8-52309c13d2cb.png"/>
</p>

# ibet-Network

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-2.7-blue.svg?cacheSeconds=2592000" />
</p>

English | [日本語](./README_JA.md)

## Overview

[ibet](https://www.ibet.jp/ibet-for-fin) is a consortium blockchain built and operated mainly by [BOOSTRY Co., Ltd.](https://boostry.co.jp/).

This repository contains the network definitions, Quorum node container definitions, and operational tooling for the environments currently provided by the ibet consortium.

## Supported Environments

This repository manages the following environments.

- `ibet-for-fin-network` : production configuration for the ibet for Fin network
- `test-network` : shared test environment for validation and operational checks
- `local-network` : local environment for development and verification

For node startup procedures and environment-specific settings, refer to the README in each directory.

## Repository Structure

- `ibet-for-fin-network/` : definitions and container assets for the ibet for Fin network
- `test-network/` : definitions and container assets for the shared test environment
- `local-network/` : docker-compose based local network for development
- `tests/` : end-to-end tests, test contracts, and supporting scripts
- `Makefile` : common commands for dependency installation, formatting, and test execution

## Technical Specifications

- Node client base: [Quorum v24.4.0](https://github.com/ConsenSys/quorum/releases/tag/v24.4.0)
- Maintained fork: [BoostryJP/quorum](https://github.com/BoostryJP/quorum)
- Consensus protocol: [QBFT](https://arxiv.org/abs/2002.03613)
- EVM version: `berlin`

Smart contracts deployed to these networks must be compiled for the `berlin` EVM.

## Versioning Policy

This repository is versioned under the following policy.

- The repository version is updated every 6 months.
- The Quorum node version is updated every 6 months. The version adopted for each scheduled update is decided by consortium agreement.
- A minor version update is used when no hard fork is required.
- A major version update is used when a hard fork is required.
- Urgent fixes may be released as revision updates outside the regular schedule.

## Participation

For details on joining the currently supported network and the latest consortium guidance, visit the official [ibet for Fin website](https://www.ibet.jp/ibet-for-fin).

## License

- The go-ethereum library is licensed under the [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html). See `COPYING.LESSER`.
- The go-ethereum binaries are licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). See `COPYING`.
