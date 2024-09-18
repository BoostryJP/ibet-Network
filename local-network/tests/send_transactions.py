import multiprocessing
import os
import sys
from datetime import datetime

path = os.path.join(os.path.dirname(__file__), "../../")
sys.path.append(path)

import secrets
import time
from coincurve import PublicKey
from eth_utils import keccak, to_checksum_address
from web3 import Web3
from web3.middleware import geth_poa_middleware
from tests.config import WEB3_HTTP_PROVIDER, CHAIN_ID
from tests.util import ContractUtils
import matplotlib.dates as mdates


def send_transactions(contract_address, start_index, num_transactions):
    contract = ContractUtils.get_contract(contract_address)
    web3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))  # general向け
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    web3.strict_bytes_type_checking = False

    for i in range(start_index, start_index + num_transactions):
        private_key = keccak(secrets.token_bytes(32))
        public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
        addr = to_checksum_address(keccak(public_key)[-20:])

        tx = contract.functions.storeString("a" * 2000).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": addr,
                "gas": 100000000,
                "gasPrice": 0,
                "nonce": 0,
            }
        )
        signed_tx = web3.eth.account.sign_transaction(
            transaction_dict=tx, private_key=private_key
        )
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction.hex())
        print(f"Sent transaction {i+1}: {tx_hash.hex()}")


def generate_transaction():
    web3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))  # general向け
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    web3.strict_bytes_type_checking = False
    while True:
        try:
            syncing = web3.eth.syncing
            if syncing:
                remaining_blocks = syncing["highestBlock"] - syncing["currentBlock"]
                if remaining_blocks == 0:
                    break
            else:
                break
        except:
            time.sleep(1)
            continue

    # Deploy
    time.sleep(10)
    args = []
    contract_address, _, _ = ContractUtils.deploy_contract(args)
    print(datetime.now().isoformat())
    print(f"DEPLOYED_CONTRACT_ADDRESS={contract_address}")

    num_processes = 5
    num_transactions_per_process = 2000

    processes = []
    for i in range(num_processes):
        start_index = i * num_transactions_per_process
        p = multiprocessing.Process(target=send_transactions, args=(contract_address, start_index, num_transactions_per_process))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while True:
        txpool_status = web3.geth.txpool.status()
        txpool_pending = txpool_status.get("pending", "0x0")
        pending_count = (
            int(txpool_pending, 16)
            if isinstance(txpool_pending, str)
            else int(txpool_pending)
        )
        if pending_count == 0:
            break
        time.sleep(1)

import matplotlib.pyplot as plt

# Web3の設定

# ブロックあたりのトランザクション数を取得
def get_transactions_and_timestamps_per_block():
    web3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))  # general向け
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    web3.strict_bytes_type_checking = False
    block_numbers = []
    transaction_counts = []
    block_timestamps = []

    block_number = web3.eth.block_number
    print(f"現在のブロック番号: {block_number}")
    start_block_number = None

    for i in range(1, block_number):
        block = web3.eth.get_block(i)
        transaction_count = len(block["transactions"])
        block_timestamp = datetime.fromtimestamp(block["timestamp"])
        if transaction_count > 0 and start_block_number is None:
            start_block_number = i


        if start_block_number is not None:
            print(f"Block {i}: {transaction_count} transactions at {block_timestamp}")

            block_numbers.append(i)
            transaction_counts.append(transaction_count)
            block_timestamps.append(block_timestamp)

    print(f"Start: {start_block_number}")
    print(f"End: {block_number}")

    return block_numbers, transaction_counts, block_timestamps


# トランザクション数をグラフにプロット
def plot_transactions_per_block(block_numbers, transaction_counts, block_timestamps, output_filename_base):
    # ブロック番号 vs トランザクション数
    plt.figure(figsize=(10, 6))
    plt.plot(block_numbers, transaction_counts, marker='o', linestyle='-', color='blue')
    plt.xlabel('Block Number')
    plt.ylabel('Transaction Count')
    plt.title('Transactions per Block (by Block Number)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{output_filename_base}_by_block_number.png')

    # タイムスタンプ vs トランザクション数
    plt.figure(figsize=(10, 6))
    plt.plot(block_timestamps, transaction_counts, marker='o', linestyle='-', color='green')

    plt.xlabel('Block Timestamp')
    plt.ylabel('Transaction Count')
    plt.title('Transactions per Block (by Block Timestamp)')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()  # 自動的に日付を回転させる

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{output_filename_base}_by_timestamp.png')

    print(f"グラフを {output_filename_base}_by_block_number.png と {output_filename_base}_by_timestamp.png に保存しました。")


# メイン関数
def main(output_filename_base):
    generate_transaction()
    block_numbers, transaction_counts, block_timestamps = get_transactions_and_timestamps_per_block()
    plot_transactions_per_block(block_numbers, transaction_counts, block_timestamps, output_filename_base)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python plot_transactions_per_block.py <output_filename>")
        sys.exit(1)

    output_filename = sys.argv[1]
    main(output_filename)
