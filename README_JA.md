# ibet-Network

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-2.2-blue.svg?cacheSeconds=2592000" />
</p>

[English](./README.md) | 日本語

<img width="33%" align="right" src="https://user-images.githubusercontent.com/963333/130191619-f1f0c342-ab8f-499d-b8f8-52309c13d2cb.png"/>

## 特徴

[ibet](https://ibet.jp/) は [株式会社BOOSTRY](https://boostry.co.jp/) が開発・運用を主導するコンソーシアムブロックチェーンです。

### 1. コンソーシアムブロックチェーン

ibet はコンソーシアム型のブロックチェーンです。
エンタープライズ向けOSSブロックチェーンプロダクトである [Quorum](https://consensys.net/quorum/) を利用して構築されています。
現在のところ、日本市場に限定して開発が行われています。

ibet は「企業」によって構成されるコンソーシアムブロックチェーンです。
コンソーシアム参加企業は自身のノード（非Validatorノード）を構築し、ネットワークに接続します。

### 2. 2つのブロックチェーン

日本法令に準拠する2つのネットワーク、"**ibet**" と "**ibet for Fin**" が存在します。
それぞれのネットワークは別々のネットワークとして構成されています。

各コンソーシアムには独立したガバナンスがあり、独自の規約とガイドラインに従って運営されています。

- **ibet** : どのような企業でも参加できるネットワークです。主に非金融商品の権利（ユーティリティトークン）が流通します。
- **ibet for Fin** : 主に金融機関のみが参加できるネットワークです。流通市場においては、認可を受けた金融機関の仲介が必要な商品が流通します。


## このリポジトリについて

このリポジトリでは、ibet コンソーシアムで定義されるネットワーク定義、
Quorumノードコンテナ（Validator、General）の管理を行います。

### リポジトリの構造

各ネットワークのネットワーク定義、ノード定義が以下のディレクトリに格納されています。

- `ibet-network` : ibet メインネットワーク
- `ibet-for-fin-network` : ibet for Fin メインネットワーク
- `test-network` : ibet テストネットワーク
- `local-network` : ローカルネットワーク

### バージョン管理方針

ibet-Networkのリポジトリは、以下の方針でバージョン管理されます。

- リポジトリ全体のバージョンアップは6ヶ月に1回行います。
- Quorumノードのバージョンアップは6ヶ月に1回行います。次回の更新で採用するバージョンは、コンソーシアムの合意により決定します。
  - ハードフォークを行わず マイナーバージョンアップ(例：1.0 -> 1.1)
  - ハードフォークあり メジャーバージョンアップ(例：1.0 -> 2.0)
- その他、緊急性の高い修正については、リビジョンアップを緊急にリリースします（例：1.1.0 -> 1.1.1）。


## Quorum バージョン

現在、ibet Network は Quorum の v23.4.0 をベースにしたノードクライアントを利用して構築されています。
ノードアプリケーションは ibet Network 向けに最適化されて、Quorum 本体のものとは部分的に異なります。
詳細は以下のプロジェクトをご参照ください。

[BoostryJP/quorum](https://github.com/BoostryJP/quorum)

## コンセンサスプロトコル

ibet ネットワークではコンセンサスプロトコルとして [QBFT](https://arxiv.org/abs/2002.03613) を利用しています。

## EVM バージョン

ibet ネットワークでは `berlin` を採用しています。
そのため、スマートコントラクトはこのバージョンでコンパイルをする必要があります。

## ibet ネットワークへの参加方法

ネットワークへの参加方法に関する詳細な情報は、[ibet 公式](https://ibet.jp/) をご確認ください。

## ライセンス

- go-ethereum 関連のライブラリは [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html) でライセンスされています。`COPYING.LESSER` のファイルを参照ください。
- go-ethereum 関連のバイナリは [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) でライセンスされています。`COPYING` のファイルを参照ください。
