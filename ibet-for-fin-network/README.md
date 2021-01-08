# ibet-for-Fin network

## Environment variable

* `PRIVATE_CONFIG` Only "ignore" can be set  
* `rpccorsdomain` Comma separated list of domains from which to accept cross origin requests (default:*)  
* `rpcvhosts` Comma separated list of virtual hostnames from which to accept requests (default: "localhost")  
* `maxpeers` Maximum number of network peers (network disabled if set to 0) (default: 50)  

## start validator node 
```
$ cd validator  
$ docker-compose up -d  
```

## start the general node 
```
$ cd general  
$ docker-compose up -d  
```

## stop validator node 
```
$ cd validator  
$ docker-compose down  
```

## stop the general node 
```
$ cd general  
$ docker-compose down  
```

