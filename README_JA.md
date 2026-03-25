<p align="center">
  <img width="33%" src="https://user-images.githubusercontent.com/963333/130191619-f1f0c342-ab8f-499d-b8f8-52309c13d2cb.png"/>
</p>

# ibet-Network

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-2.8-blue.svg?cacheSeconds=2592000" />
</p>

[English](./README.md) | 日本語

## 概要

[ibet](https://ibet.jp/) は、[株式会社BOOSTRY](https://boostry.co.jp/) が開発・運用を主導するコンソーシアムブロックチェーンです。

このリポジトリでは、現在 ibet コンソーシアムで提供している各環境のネットワーク定義、Quorumノードコンテナ定義、および運用・検証用ツールを管理しています。

## 対応環境

このリポジトリで管理している環境は以下のとおりです。

- `ibet-for-fin-network` : ibet for Fin 本番環境向けの設定
- `test-network` : 検証および運用確認に利用する共有テスト環境
- `local-network` : 開発およびローカル検証向け環境

ノードの起動手順や環境固有の設定は、各ディレクトリ配下のREADMEを参照してください。

## リポジトリ構成

- `ibet-for-fin-network/` : ibet for Fin 向けの定義ファイルとコンテナ関連資産
- `test-network/` : 共有テスト環境向けの定義ファイルとコンテナ関連資産
- `local-network/` : docker-compose ベースのローカル開発環境
- `tests/` : E2Eテスト、テストコントラクト、補助スクリプト
- `Makefile` : 依存関係の導入、整形、テスト実行用の共通コマンド

## 技術仕様

- ノードクライアントのベース: [Quorum v24.4.0](https://github.com/ConsenSys/quorum/releases/tag/v24.4.0)
- 利用しているフォーク: [BoostryJP/quorum](https://github.com/BoostryJP/quorum)
- コンセンサスプロトコル: [QBFT](https://arxiv.org/abs/2002.03613)
- EVMバージョン: `berlin`

これらのネットワークにデプロイするスマートコントラクトは、`berlin` 向けにコンパイルする必要があります。

## バージョン管理方針

このリポジトリは、以下の方針でバージョン管理されます。

- リポジトリ全体のバージョンアップは 6 か月に 1 回行います。
- Quorumノードのバージョンアップは 6 か月に 1 回行い、採用バージョンはコンソーシアムの合意により決定します。
- ハードフォークを伴わない場合はマイナーバージョンアップを行います。
- ハードフォークを伴う場合はメジャーバージョンアップを行います。
- 緊急性の高い修正は、定期更新とは別にリビジョンアップとしてリリースする場合があります。

## ネットワーク参加方法

現在サポート対象となっているネットワークへの参加方法や最新のコンソーシアム案内については、[ibet for Fin 公式](https://www.ibet.jp/ibet-for-fin) を確認してください。

## ライセンス

- go-ethereum 関連ライブラリは [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html) でライセンスされています。`COPYING.LESSER` を参照してください。
- go-ethereum 関連バイナリは [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) でライセンスされています。`COPYING` を参照してください。
