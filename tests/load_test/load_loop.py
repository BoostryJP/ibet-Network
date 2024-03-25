"""
Copyright BOOSTRY Co., Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

import os
import secrets
import sys

from coincurve import PublicKey
from eth_utils import keccak, to_checksum_address
from web3 import Web3
from web3.middleware import geth_poa_middleware

path = os.path.join(os.path.dirname(__file__), "../../")
sys.path.append(path)

from tests.config import CHAIN_ID, DEPLOYED_CONTRACT_ADDRESS, WEB3_HTTP_PROVIDER
from tests.util import ContractUtils

contract = ContractUtils.get_contract(DEPLOYED_CONTRACT_ADDRESS)
web3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3.strict_bytes_type_checking = False


for i in range(10000):
    private_key = keccak(secrets.token_bytes(32))
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = to_checksum_address(keccak(public_key)[-20:])
    nonce = web3.eth.get_transaction_count(addr)
    tx = contract.functions.loop10000().build_transaction(
        transaction={
            "chainId": CHAIN_ID,
            "from": addr,
            "gas": 100000000,
            "gasPrice": 0,
            "nonce": nonce,
        }
    )
    signed_tx = web3.eth.account.sign_transaction(
        transaction_dict=tx, private_key=private_key
    )
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction.hex())
