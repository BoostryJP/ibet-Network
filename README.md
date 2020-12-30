# ibet-Quorum

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
</p>

## About ibet

[ibet](https://ibet.jp/) is a consortium blockchain built and operated mainly by BOOSTRY Co., Ltd. .

### 1. Consortium blockchain

ibet is a consortium blockchain. 
It is built using [Quorum](https://consensys.net/quorum/), an OSS blockchain for enterprise. 
Currently, it is being developed only for the Japanese market.

ibet is a consortium blockchain made up of "companies". 
Each company in the consortium builds its own node (non-Validator node) and connects it to the network.

### 2. Two networks

There are two consortium networks, "ibet" and "ibet for Fin", in compliance with Japanese laws and regulations.
Each of them constitutes its own blockchain network.

Each consortium has its own independent governance and operates according to its own terms of reference and guidelines.

- **ibet** : A network in which any company can participate. Mainly non-financial rights (utility tokens) are distributed.
- **ibet for Fin** : A network in which mainly only financial institutions can participate. Products that require the intermediation of licensed financial institutions in the secondary market are distributed.

## License

- The go-ethereum library is licensed under the
[GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html), also
included in our repository in the `COPYING.LESSER` file.

- The go-ethereum binaries is licensed under the
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), also included
in our repository in the `COPYING` file.


<!-- 
## Quickstart

### 1. docker-ceのインストール
事前に、Docker実行環境を構築する。


### 2. quorumコンテナ作成

* Validatorノードのビルド

```bash
cd quorum-prod
docker build -t quorum .
```

* Generalノードの場合

```bash
cd quorum-prod-general
docker build -t quorum .
```


### 3. 初期ネットワークの作成（istanbul-toolsを利用）
* ノード情報を作成するためistanbul-toolsを利用する。
* 導入にはGolangが必要。Golangのバージョンを1.7以降にしなければ、Makeエラーが発生するので注意。

```bash
git clone https://github.com/getamis/istanbul-tools
```

* 以下のように実行する。

```bash
cd /home/ubuntu/gowork/src/github.com/getamis/istanbul-tools
./build/bin/istanbul setup --num 4 --nodes --verbose --quorum
```

* 生成された情報をもとに、genesis.json,static-nodes.jsonを修正する。
* genesis.jsonとstatic-nodes.jsonをdatadir配下に格納する。

```
/home/ubuntu/quorum-data/genesis.json
/home/ubuntu/quorum-data/geth/static-nodes.json
```
-->
