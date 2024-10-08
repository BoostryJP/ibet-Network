# local network

You can use the docker-compose file which runs on Ubuntu.
Please edit the docker-compose file to suit your environment and use it.

By running this docker-compose, the Validator node will start with 4 nodes. 
Please check the file itself for detailed configuration.

## Starting and Stopping the Server
You can start the local network with:
```
$ docker-compose up -d
```

You can stop the local network with:
```
$ docker-compose stop
```

## Migrate from IBFT to QBFT
You can migrate an existing IBFT network to a QBFT network with the following steps:

1. Stop the network.
2. Update the docker-compose file with a non-zero `testQBFTBlock`.
 For example, if the current block number in your IBFT network is 100, set `testQBFTBlock` to any block greater than 100, and once that fork block is reached, QBFT consensus will be used instead of IBFT.
3. Restart the network.

## Berlin hardfork setting
You can migrate an existing network to a Berlin hardfork network with the following steps:

1. Stop the network.
2. Update the docker-compose file with a non-zero `berlinBlock`.
 Set a future block number rather than the current block number.
3. Restart the network.

## Introducing Empty Block Period Seconds
You can introduce empty block period to an existing network with the following steps:

1. Stop the network.
2. Update the docker-compose file with a non-zero `emptyBlockPeriodIntroduceBlock`.
 Set a future block number rather than the current block number.
3. Restart the network.
