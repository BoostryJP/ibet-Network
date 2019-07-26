# tmr-quorum
---
## 1.事前準備
### 1.1 docker-ceのインストール
- 下記を参考
https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository

```
git clone https://github.com/N-Village/tmr-docker.git
cd tmr-docker
./installer/docker-installer.sh

# ubuntuユーザでdockerコマンドを利用する場合に実行。passwordがない環境の場合は、再ログインが必要。
su - $USER
```

## 1.2. quorumコンテナ作成(prod環境向け)
### 1.2.1. docker image作成
- validatorの場合
```
cd quorum-prod
docker build -t quorum .
```

- generalの場合
```
cd quorum-prod-general
docker build -t quorum .
```

### 1.2.2. istanbul用ノードの設定
- ノード情報を作成するためistanbul-toolsを実行させる。
- istanbul-toolsをcloneする
- clone https://github.com/getamis/istanbul-tools

* 導入にはgoが必要
Golangのバージョンが1.7以降にしなければMakeエラーが発生する  
Ubuntu16.04LTSのapt-getではいるGolangのバージョンのデフォルトは1.6x  
明示的にapt-get installで1.7以降を取得する必要がある  
```
$ sudo apt-get install golang-1.9
```
この方法で入れると/user/bin/goからのシンボリックが通っていないのでgo versionをしてもエラーとなる  
明示的にシンボリックリンクを設定すること
```
$ sudo ln -s /usr/lib/go-1.9/bin/go /usr/bin/go
$ go version
```
- 下記の通り、Buildを実行
```
cd /home/ubuntu/gowork/src/github.com/getamis/istanbul-tools
./build/bin/istanbul setup --num 4 --nodes --verbose --quorum
```
- 生成された情報をもとに、genesis.json,static-nodes.jsonを修正
- genesis.jsonとstatic-nodes.jsonをdatadir配下に格納する
```
/home/ubunts/quorum-data/genesis.json
/home/ubunts/quorum-data/geth/stati-cnodes.json
```

# 2.Quorumネットワーク構築
## 2.1. quorum設定・起動
-ノード稼動環境のIPアドレスに合わせて、static-nodes.jsonのIPアドレスを修正する。
- 修正後、下記コマンドを実行。引数はノードA~Dで変更する。
```
./quorum-init.sh A
./quorum-start.sh

# 稼動確認
tail -f qdata/logs/geth.log
```

## 2.2 account作成
- validator にアクセスし、アカウントを作成する
```
# gethにattach
docker exec -it quorum geth attach qdata/dd/geth.ipc

# アンロック
personal.unlockAccount(eth.accounts[0], "nvillage201803+", 1000)

# 登録後のコントラクト確認
eth.contract(<contract_address>)
```
## 2.3 node追加
追加するノードがvalidatorの場合、2f+1のvalidatorノードで実施。追加するノードがgeneralの場合、既存ノード1つで実施。  
```
./installer/quorum-add-node.sh <enode id> <coinbase> <NODE_TYPE>

# 例
./installer/quorum-add-node.sh enode://61b6504917fe9e0a195d9d1aaa585cc77422fe3fa73df82df844a714ba96c703013698ceeddaffce16eabfceb8d8203d2e51cc3065f4356fea04c19049271a92@10.0.0.15:21000?discport=0 0x4eeb101c248799982be84af6bf16cbac97f1882d validator
```
## 2.4 node削除
./installer/quorum-remove-node.sh <enode id> <coinbase> <NODE_TYPE>
```
./installer/quorum-remove-node.sh <enode id> <coinbase> <NODE_TYPE>

# 例
./installer/quorum-remove-node.sh enode://61b6504917fe9e0a195d9d1aaa585cc77422fe3fa73df82df844a714ba96c703013698ceeddaffce16eabfceb8d8203d2e51cc3065f4356fea04c19049271a92@10.0.0.15:21000?discport=0 0x4eeb101c248799982be84af6bf16cbac97f1882d validator
```
