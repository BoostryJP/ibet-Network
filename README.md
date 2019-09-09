# tmr-quorum

## 1. docker-ceのインストール
- 下記を参考
- https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository

```
git clone https://github.com/N-Village/tmr-docker.git
cd tmr-docker
./installer/docker-installer.sh

# ubuntuユーザでdockerコマンドを利用する場合に実行。passwordがない環境の場合は、再ログインが必要。
su - $USER
```

## 2. quorumコンテナ作成
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

## 3. 初期ネットワークの作成（istanbul-toolsを利用）
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

- この方法で入れると/user/bin/goからのシンボリックが通っていないのでgo versionをしてもエラーとなる  
- 明示的にシンボリックリンクを設定すること

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
/home/ubuntu/quorum-data/genesis.json
/home/ubuntu/quorum-data/geth/static-nodes.json
```
