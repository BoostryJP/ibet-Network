# Network non-degrade test

This document describes how to run network end-to-end non-degrade tests.

## Prerequisites

- Need to set up a `local-network` beforehand (see [instructions](https://github.com/BoostryJP/ibet-Network/tree/develop/local-network)).
- E2E tests are run using pytest. Therefore, Python runtime environment is required.
  - 3.11 or greater.

## Setting environment variables

- `SOLC_VERSION_PRAGMA` - Solc version 
  - default => `^0.8.0`
- `WEB3_HTTP_PROVIDER` - Quorum JSON-RPC server endpoint
  - default => `http://localhost:8545`
  
## Running the tests

### Install python packages

```shell
$ make install
```

### Compile the test contract

The contract code to be tested is `tests/contracts/E2ETest.sol`.

Compile the contract code.

````shell
$ poetry run python compile.py
````

After successful completion, `E2ETest.json` will be created in tests/contracts.

### Deploy the contract

Deploy the contract with the following command.

```shell
$ poetry run python deploy.py
DEPLOYED_CONTRACT_ADDRESS=0x79448CB02a0F8cff71005963075187aAD9a050f3
$ export DEPLOYED_CONTRACT_ADDRESS=0x79448CB02a0F8cff71005963075187aAD9a050f3
```

### Running the e2e tests

```shell
$ poetry run pytest . -vv
```
