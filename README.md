# ibet-Quorum

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

## License

The go-ethereum library (i.e. all code outside of the `cmd` directory) is licensed under the
[GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html), also
included in our repository in the `COPYING.LESSER` file.

The go-ethereum binaries (i.e. all code inside of the `cmd` directory) is licensed under the
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), also included
in our repository in the `COPYING` file.
